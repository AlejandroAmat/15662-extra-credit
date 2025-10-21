import pygame
import math
from shape import Shape

class Display:
    def __init__(self, width=800, height=600):
        pygame.init()
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Shape Drag / Anchor / Rotate / Scale")
        self.clock = pygame.time.Clock()
        self.shape = None
        self.dragging_shape = False
        self.dragging_anchor = False
        self.rotating_shape = False
        self.scaling_shape = False
        self.scaling_edge = None
        self.drag_offset = pygame.Vector2()
        self.start_angle = 0
        self.start_width = 0
        self.start_height = 0
        self.start_mouse_pos = None
        self.running = True
        self.creating_shape = False

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    self.creating_shape = True
                    print("Click to create a new shape.")

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_pos = pygame.Vector2(event.pos)

                    if self.creating_shape:
                        self.shape = Shape(mouse_pos)
                        self.creating_shape = False
                        print("Shape created.")
                        continue

                    if self.shape:
                        if self.shape.is_over_anchor(mouse_pos):
                            self.dragging_anchor = True
                            self.drag_offset = self.shape.anchor - mouse_pos

                        elif self.shape.is_over_corner(mouse_pos):
                            self.rotating_shape = True
                            v1 = mouse_pos - self.shape.anchor
                            self.start_angle = math.atan2(v1.y, v1.x) - self.shape.rotation

                        elif (midpoint_idx := self.shape.is_over_midpoint(mouse_pos)) is not None:
                            self.scaling_shape = True
                            self.scaling_edge = midpoint_idx
                            self.start_width = self.shape.width
                            self.start_height = self.shape.height
                            self.start_mouse_pos = mouse_pos

                        elif self.shape.contains_point(mouse_pos):
                            self.dragging_shape = True
                            self.drag_offset = self.shape.center - mouse_pos

            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    self.dragging_shape = False
                    self.dragging_anchor = False
                    self.rotating_shape = False
                    self.scaling_shape = False
                    self.scaling_edge = None


            elif event.type == pygame.MOUSEMOTION:
                mouse_pos = pygame.Vector2(event.pos)
                if self.dragging_shape and self.shape:
                    delta = pygame.Vector2(event.rel)
                    self.shape.move(delta)

                elif self.dragging_anchor and self.shape:
                    self.shape.set_anchor(mouse_pos + self.drag_offset)

                elif self.rotating_shape and self.shape:
                    v2 = mouse_pos - self.shape.anchor
                    new_angle = math.atan2(v2.y, v2.x)
                    self.shape.rotation = new_angle - self.start_angle

                elif self.scaling_shape and self.shape:
                    delta = mouse_pos - self.start_mouse_pos
                    
                    local_delta = delta.rotate_rad(-self.shape.rotation)
                    
                    if self.scaling_edge == 0 or self.scaling_edge == 2:  
                        scale = 1 + (2 * local_delta.y / self.start_height) if self.scaling_edge == 2 else 1 - (2 * local_delta.y / self.start_height)
                        new_height = max(10, self.start_height * scale)
                        
                        center_rel = self.shape.center - self.shape.anchor
                        center_rel_local = center_rel.rotate_rad(-self.shape.rotation)
                        
                        center_rel_local.y *= (new_height / self.shape.height)
                        
                        center_rel_scaled = center_rel_local.rotate_rad(self.shape.rotation)
                        self.shape.center = self.shape.anchor + center_rel_scaled
                        self.shape.height = new_height
                        
                    else: 
                        scale = 1 + (2 * local_delta.x / self.start_width) if self.scaling_edge == 1 else 1 - (2 * local_delta.x / self.start_width)
                        new_width = max(10, self.start_width * scale)
                     
                        center_rel = self.shape.center - self.shape.anchor
                        center_rel_local = center_rel.rotate_rad(-self.shape.rotation)
                        
                        center_rel_local.x *= (new_width / self.shape.width)
                        
                        center_rel_scaled = center_rel_local.rotate_rad(self.shape.rotation)
                        self.shape.center = self.shape.anchor + center_rel_scaled
                        self.shape.width = new_width

    def draw(self):
        self.screen.fill((30, 30, 30))
        
        font = pygame.font.Font(None, 24)
        instructions = [
            "Press 'C' and then click to create a shape",
            "Red dot: Drag to move anchor",
            "Yellow corners: Drag to rotate",
            "Blue midpoints: Drag to scale",
            "Shape body: Drag to move everything"
        ]
        
        y_offset = 10
        for text in instructions:
            text_surface = font.render(text, True, (200, 200, 200))
            self.screen.blit(text_surface, (10, y_offset))
            y_offset += 25
        
        if self.shape:
            self.shape.draw(self.screen)
        pygame.display.flip()

    def run(self):
        while self.running:
            self.handle_events()
            self.draw()
            self.clock.tick(60)
        pygame.quit()