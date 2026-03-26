# FSM-Redstone-Synthesizer
# Copyright (C) 2025-2026  Cristian-Ioan-George Chira (github.com/chiracristian)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free-Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

from blocks import *

# X+ goes EAST
# X- goes WEST
# Y+ goes UP
# Y- goes DOWN
# Z+ goes SOUTH
# Z- goes NORTH

class BlockGridException(Exception):
    pass

class BlockGrid:
    def __init__(self, size_x: int, size_y: int, size_z: int):
        self.size: tuple[int, int, int] = (size_x, size_y, size_z)
        self.origin: tuple[int, int, int] = (0, 0, 0)

        # Store the blocks into a 3D array
        self.blocks = [[[Block(AIR)
                         for _ in range(size_z)]
                         for _ in range(size_y)]
                         for _ in range(size_x)]
        
        # Store the total delay of torches and repeaters
        self.delay = 0

        # Store the position of torches (to be propagated)
        self.torches_pos: list[tuple[int, int, int]] = []
        
    def is_out_of_bounds(self, x: int, y: int, z: int) -> bool:
        return not (0 <= x < self.size[0] and 0 <= y < self.size[1] and 0 <= z < self.size[2])
        

    def set_wire_connection(self, x: int, y: int, z: int, direction: str, state: WireConnection):
        block = self.blocks[x][y][z]
        if isinstance(block, Wire):
            if direction == "north": block.north_connection = state
            elif direction == "south": block.south_connection = state
            elif direction == "east":  block.east_connection = state
            elif direction == "west":  block.west_connection = state

    def propagate_power_through_wires(self, x: int, y: int, z: int, power: int = MAX_WIRE_POWER):
        # Bounds check
        if self.is_out_of_bounds(x, y, z):
            return

        block = self.blocks[x][y][z]
        
        # Only propagate through wires
        if not isinstance(block, Wire):
            return
        
        # Stop if power is exhausted
        if power <= 0:
            return

        # Only proceed if we are actually increasing the power level
        if block.power >= power:
            return

        # Set the power
        block.power = power

        # Map connections to relative coordinate offsets
        # Connection name -> (dx, dy_offset, dz)
        directions = {
            Directions.NORTH: (0, 0, -1),
            Directions.SOUTH: (0, 0, 1),
            Directions.EAST:  (1, 0, 0),
            Directions.WEST:  (-1, 0, 0)
        }

        states = block.get_block_states()

        for side, (dx, dy, dz) in directions.items():
            conn_type = states.get(side.value)

            nx, ny, nz = 0, 0, 0
            check_down = False

            if conn_type == WireConnection.SIDE.value:
                # Flat connection
                nx, ny, nz = x + dx, y, z + dz
                check_down = True
            elif conn_type == WireConnection.UP.value:
                # Climbing up a block
                nx, ny, nz = x + dx, y + 1, z + dz

            # Propagate through the connection
            self.propagate_power_through_wires(nx, ny, nz, power - 1)

            # Propagate through repeater, if facing correspondingly
            if isinstance(self.blocks[nx][ny][nz], Repeater):
                if self.blocks[nx][ny][nz].facing == opposite_direction(side):
                    self.propagate_power_from_repeater(nx, ny, nz)
            
            # Redstone automatically connects down if there is a wire below 
            # and no solid block in the way.
            if check_down and not self.is_out_of_bounds(nx, ny, nz):
                if y > 0 and self.blocks[nx][ny][nz].name == AIR:
                    down_block = self.blocks[nx][ny - 1][nz]
                    if isinstance(down_block, Wire):
                        self.propagate_power_through_wires(nx, ny - 1, nz, power - 1)

    def propagate_all_torches(self):
        for torch_pos in self.torches_pos:
            self.propagate_power_from_torch(torch_pos[0], torch_pos[1], torch_pos[2])

    def propagate_power_from_torch(self, x: int, y: int, z: int):
        block = self.blocks[x][y][z]
        if not isinstance(block, Torch) or not block.lit:
            return

        # Torch powers neighbors
        neighbors = [
            (x + 1, y, z), (x - 1, y, z),
            (x, y + 1, z), (x, y - 1, z),
            (x, y, z + 1), (x, y, z - 1)
        ]

        # If the torch is a WALL torch, it does NOT power the block it is attached to
        # (The block at the opposite direction of its 'facing' state)
        if block.torch_type == TorchType.WALL:
            # facing directions: NORTH means attached to SOUTH face of a block
            attach_offsets = {
                Directions.NORTH: (0, 0, 1),
                Directions.SOUTH: (0, 0, -1),
                Directions.EAST:  (-1, 0, 0),
                Directions.WEST:  (1, 0, 0)
            }
            forbidden = attach_offsets.get(block.facing)
            if forbidden:
                fx, fy, fz = forbidden
                neighbors = [n for n in neighbors if n != (x + fx, y + fy, z + fz)]

        for nx, ny, nz in neighbors:
            if not self.is_out_of_bounds(nx, ny, nz):
                self.propagate_power_through_wires(nx, ny, nz, MAX_WIRE_POWER)

    def propagate_power_from_repeater(self, x: int, y: int, z: int):
        block = self.blocks[x][y][z]
        if not isinstance(block, Repeater):
            return
        
        # The repeater gets powered
        block.powered = True

        # A repeater outputs power 15 in its 'facing' direction
        offsets = {
            Directions.NORTH: (0, 0, 1),
            Directions.SOUTH: (0, 0, -1),
            Directions.EAST:  (-1, 0, 0),
            Directions.WEST:  (1, 0, 0)
        }
        
        dx, dy, dz = offsets.get(block.facing, (0, 0, 0))
        nx, ny, nz = x + dx, y, z + dz

        # Propagate at the same height
        if not self.is_out_of_bounds(nx, ny, nz):
            self.propagate_power_through_wires(nx, ny, nz, MAX_WIRE_POWER)
        
        # Propagate one block higher
        if not self.is_out_of_bounds(nx, ny + 1, nz):
            self.propagate_power_through_wires(nx, ny + 1, nz, MAX_WIRE_POWER)

    def paste(self, pasted_grid: "BlockGrid", 
              offset_x: int, offset_y: int, offset_z: int,
              allow_overwriting: bool = False):
        
        sx, sy, sz = pasted_grid.size
        ox, oy, oz = pasted_grid.origin

        # Iterate over blocks in pasted region space
        for x in range(sx):
            for y in range(sy):
                for z in range(sz):
                    block = pasted_grid.blocks[x][y][z]

                    # Ignore air blocks
                    if block.name == AIR:
                        continue

                    # Absolute coordinates in the grid
                    gx = offset_x + (x - ox)
                    gy = offset_y + (y - oy)
                    gz = offset_z + (z - oz)

                    # Bounds check
                    if not (0 <= gx < self.size[0] and 0 <= gy < self.size[1] and 0 <= gz < self.size[2]):
                        raise BlockGridException(f"Block at ({gx},{gy},{gz}) is out of grid bounds. \
                                                 Size is ({self.size[0]},{self.size[1]},{self.size[2]})")
                    
                    # Collision check
                    if (not allow_overwriting) and self.blocks[gx][gy][gz].name != "minecraft:air":
                        raise BlockGridException(f"Cannot paste block at ({gx},{gy},{gz}): space occupied.")
                    
                    # Paste the block
                    self.blocks[gx][gy][gz] = block

        # If the pasted region has torches tracked, include them
        for tx, ty, tz in pasted_grid.torches_pos:
            # Apply the same translation logic used for blocks
            master_tx = offset_x + (tx - ox)
            master_ty = offset_y + (ty - oy)
            master_tz = offset_z + (tz - oz)
            
            self.torches_pos.append((master_tx, master_ty, master_tz))
