"""

2D Highway Driving Game - Overtaking Style
A realistic highway driving game where you overtake slower traffic

Controls:
- Arrow Keys OR WASD: Control car
  * UP/W: Speed up
  * DOWN/S: Slow down
  * LEFT/A: Change lane left
  * RIGHT/D: Change lane right
- ESC: Quit game

By Prem Patel (Refactored for realistic overtaking gameplay)
"""

import sys
import random
import pygame

pygame.init()

# ============================================================
#                   Global Configuration
# ============================================================

# Screen & Road
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
ROAD_WIDTH = 500
ROAD_X = (SCREEN_WIDTH - ROAD_WIDTH) // 2

LANE_COUNT = 3
LANE_WIDTH = ROAD_WIDTH // LANE_COUNT

# Car dimensions
CAR_WIDTH, CAR_HEIGHT = 40, 70

# Colors
BG_COLOR = (34, 139, 34)        # Grass green
ROAD_COLOR = (60, 60, 60)       # Dark gray road
LINE_COLOR = (255, 255, 100)    # Yellow lines
CAR_COLOR = (220, 20, 60)       # Crimson red player car
OBSTACLE_COLOR = (30, 144, 255) # Dodger blue traffic
TEXT_COLOR = (255, 255, 255)    # White

# Game settings
PLAYER_BASE_SPEED = 0           # Player's forward speed
MIN_PLAYER_SPEED = 0
MAX_PLAYER_SPEED = 20
TRAFFIC_MIN_SPEED = 5          # Slower traffic to overtake
TRAFFIC_MAX_SPEED = 9
SPAWN_INTERVAL = 1800           # milliseconds between spawns

# ============================================================
#                    Traffic Car Class
# ============================================================

class TrafficCar:
    """Represents slower traffic cars to overtake."""
    
    def __init__(self, lane):
        self.width = 40
        self.height = 70
        self.speed = random.uniform(TRAFFIC_MIN_SPEED, TRAFFIC_MAX_SPEED)
        self.color = OBSTACLE_COLOR
        self.lane = lane
        
        # Position in the specified lane
        self.x = ROAD_X + lane * LANE_WIDTH + (LANE_WIDTH - self.width) // 2
        # Spawn ahead of player (at top of screen)
        self.y = -self.height
    
    def update(self, player_speed):
        """
        Update position relative to player's speed.
        Traffic moves slower, so player appears to overtake them.
        """
        # Relative speed = player speed - traffic speed
        # This makes traffic appear to move backward relative to player
        self.y += player_speed - self.speed
    
    def check_collision_with_traffic(self, other_cars):
        """
        Check if this car is colliding with other traffic cars.
        Adjust speed to maintain safe distance (realistic physics).
        """
        my_rect = self.get_rect()
        
        for other in other_cars:
            if other is self:  # Don't check collision with self
                continue
            
            # Only check cars in the same lane
            if other.lane == self.lane:
                other_rect = other.get_rect()
                
                # Check if cars are too close (within collision range)
                # We need to check vertical distance
                vertical_distance = abs(self.y - other.y)
                
                # If too close and this car is behind the other
                if vertical_distance < self.height + 10 and self.y > other.y:
                    # Match speed with car ahead to maintain safe distance
                    self.speed = min(self.speed, other.speed)
                    # Maintain minimum gap
                    if vertical_distance < self.height + 5:
                        self.y = other.y + other.height + 5
    
    def draw(self, screen):
        """Render the traffic car with realistic appearance."""
        cx, cy = int(self.x), int(self.y)
        
        # Shadow
        shadow = pygame.Surface((self.width + 3, self.height + 3), pygame.SRCALPHA)
        pygame.draw.rect(shadow, (0, 0, 0, 50), (0, 0, self.width + 3, self.height + 3), border_radius=6)
        screen.blit(shadow, (cx - 1, cy + 2))
        
        # Main body with rounded corners
        pygame.draw.rect(screen, self.color, (cx, cy, self.width, self.height), border_radius=5)
        
        # Body highlight
        highlight = (60, 170, 255)
        pygame.draw.rect(screen, highlight, (cx + 2, cy + 2, self.width - 4, self.height - 4), border_radius=4)
        
        # Roof
        roof_color = (20, 100, 180)
        pygame.draw.rect(screen, roof_color, (cx + 8, cy + 20, self.width - 16, 30), border_radius=3)
        
        # Front windshield (angled)
        windshield = (150, 220, 255)
        pygame.draw.polygon(screen, (100, 150, 200), [
            (cx + 8, cy + 8), (cx + 32, cy + 8), (cx + 28, cy + 22), (cx + 12, cy + 22)
        ])
        pygame.draw.polygon(screen, windshield, [
            (cx + 10, cy + 10), (cx + 30, cy + 10), (cx + 27, cy + 21), (cx + 13, cy + 21)
        ])
        
        # Rear windshield
        pygame.draw.polygon(screen, (100, 150, 200), [
            (cx + 12, cy + 48), (cx + 28, cy + 48), (cx + 32, cy + 62), (cx + 8, cy + 62)
        ])
        pygame.draw.polygon(screen, windshield, [
            (cx + 13, cy + 49), (cx + 27, cy + 49), (cx + 30, cy + 61), (cx + 10, cy + 61)
        ])
        
        # Headlights
        pygame.draw.ellipse(screen, (255, 255, 150), (cx + 6, cy + 2, 8, 5))
        pygame.draw.ellipse(screen, (255, 255, 150), (cx + 26, cy + 2, 8, 5))
        
        # Taillights
        pygame.draw.ellipse(screen, (200, 0, 0), (cx + 6, cy + 63, 8, 5))
        pygame.draw.ellipse(screen, (200, 0, 0), (cx + 26, cy + 63, 8, 5))
        
        # Side mirrors
        pygame.draw.rect(screen, (120, 120, 120), (cx - 2, cy + 28, 3, 6))
        pygame.draw.rect(screen, (120, 120, 120), (cx + 39, cy + 28, 3, 6))
    
    def get_rect(self):
        """Return collision rectangle."""
        return pygame.Rect(int(self.x), int(self.y), self.width, self.height)
    
    def is_off_screen(self):
        """Check if car has moved past the bottom of screen."""
        return self.y > SCREEN_HEIGHT
    
    def is_near_top(self, threshold=200):
        """Check if car is still near the top of screen."""
        return self.y < threshold


# ============================================================
#                   Highway Game Class
# ============================================================

class HighwayGame:
    """Main game class handling overtaking gameplay."""
    
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Highway Overtaking Game")
        
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        
        # Setup traffic spawn timer
        self.SPAWN_EVENT = pygame.USEREVENT + 1
        pygame.time.set_timer(self.SPAWN_EVENT, SPAWN_INTERVAL)
        
        self.reset()
    
    def reset(self):
        """Reset game state."""
        self.lane_index = 1  # Start in middle lane
        self.target_lane = 1  # Lane we're moving towards
        self.car_x_offset = 0  # Smooth position offset for lane transitions
        self.car_y = SCREEN_HEIGHT - 150  # Player position
        self.speed = PLAYER_BASE_SPEED
        self.road_offset = 0
        self.traffic = []
        self.score = 0
        self.overtakes = 0  # Count successful overtakes
        self.game_over = False
        self.is_changing_lane = False
    
    def handle_input(self):
        """Process keyboard input for speed control."""
        keys = pygame.key.get_pressed()
        
        # Speed control - Arrow keys OR WASD
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.speed = min(self.speed + 0.15, MAX_PLAYER_SPEED)
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.speed = max(self.speed - 0.15, MIN_PLAYER_SPEED)
    
    def handle_lane_change(self, event):
        """Handle lane change input with key press events - Arrow keys OR WASD."""
        if event.type == pygame.KEYDOWN and not self.is_changing_lane:
            # Left lane change: LEFT arrow OR A key
            if (event.key == pygame.K_LEFT or event.key == pygame.K_a) and self.target_lane > 0:
                self.target_lane -= 1
                self.is_changing_lane = True
            # Right lane change: RIGHT arrow OR D key
            elif (event.key == pygame.K_RIGHT or event.key == pygame.K_d) and self.target_lane < LANE_COUNT - 1:
                self.target_lane += 1
                self.is_changing_lane = True
    
    def update(self):
        """Update game state."""
        if self.game_over:
            return
        
        # Smooth lane transition
        if self.is_changing_lane:
            target_x = ROAD_X + self.target_lane * LANE_WIDTH + (LANE_WIDTH - CAR_WIDTH) // 2
            current_x = ROAD_X + self.lane_index * LANE_WIDTH + (LANE_WIDTH - CAR_WIDTH) // 2 + self.car_x_offset
            
            transition_speed = 8
            
            if abs(target_x - current_x) < transition_speed:
                self.lane_index = self.target_lane
                self.car_x_offset = 0
                self.is_changing_lane = False
            else:
                if target_x > current_x:
                    self.car_x_offset += transition_speed
                else:
                    self.car_x_offset -= transition_speed
        
        # Update traffic cars
        player_rect = self.get_car_rect()
        
        # First pass: Check traffic-to-traffic collisions (realistic physics)
        for car in self.traffic:
            car.check_collision_with_traffic(self.traffic)
        
        # Second pass: Update positions
        for car in self.traffic[:]:
            old_y = car.y
            car.update(self.speed)
            
            # Check if we successfully overtook this car
            if old_y < self.car_y and car.y >= self.car_y and not car.is_off_screen():
                self.overtakes += 1
                self.score += 15  # Bonus for overtaking
            
            # Remove cars that went off screen
            if car.is_off_screen():
                self.traffic.remove(car)
                self.score += 5  # Small score for distance
        
        # Check collisions
        for car in self.traffic:
            if player_rect.colliderect(car.get_rect()):
                self.game_over = True
                break
        
        # Update road animation - moves backward since we're moving forward
        self.road_offset = (self.road_offset + self.speed) % 50
    
    def get_car_rect(self):
        """Get player car's collision rectangle with smooth lane transitions."""
        x = ROAD_X + self.lane_index * LANE_WIDTH + (LANE_WIDTH - CAR_WIDTH) // 2 + self.car_x_offset
        return pygame.Rect(int(x), self.car_y, CAR_WIDTH, CAR_HEIGHT)
    
    def draw_road(self):
        """Render the road and lane markings."""
        # Grass background
        self.screen.fill(BG_COLOR)
        
        # Road surface
        pygame.draw.rect(self.screen, ROAD_COLOR, (ROAD_X, 0, ROAD_WIDTH, SCREEN_HEIGHT))
        
        # Road borders
        pygame.draw.line(self.screen, LINE_COLOR, (ROAD_X, 0), (ROAD_X, SCREEN_HEIGHT), 4)
        pygame.draw.line(self.screen, LINE_COLOR, 
                        (ROAD_X + ROAD_WIDTH, 0), (ROAD_X + ROAD_WIDTH, SCREEN_HEIGHT), 4)
        
        # Lane markings (animated dashed lines moving backward)
        dash_height = 30
        gap = 20
        
        for lane in range(1, LANE_COUNT):
            x = ROAD_X + lane * LANE_WIDTH
            for y in range(-dash_height, SCREEN_HEIGHT, dash_height + gap):
                pygame.draw.line(
                    self.screen, LINE_COLOR,
                    (x, y + self.road_offset),
                    (x, y + dash_height + self.road_offset), 3
                )
    
    def draw_car(self):
        """Render the player's car with realistic details."""
        car_rect = self.get_car_rect()
        cx, cy = car_rect.x, car_rect.y
        
        # Shadow effect
        shadow = pygame.Surface((CAR_WIDTH + 4, CAR_HEIGHT + 4), pygame.SRCALPHA)
        pygame.draw.rect(shadow, (0, 0, 0, 60), (0, 0, CAR_WIDTH + 4, CAR_HEIGHT + 4), border_radius=8)
        self.screen.blit(shadow, (cx - 2, cy + 2))
        
        # Main car body with rounded corners
        pygame.draw.rect(self.screen, CAR_COLOR, car_rect, border_radius=6)
        
        # Car body highlights (3D effect)
        highlight_color = (255, 60, 90)
        pygame.draw.rect(self.screen, highlight_color, 
                        (cx + 2, cy + 2, CAR_WIDTH - 4, CAR_HEIGHT - 4), border_radius=5)
        
        # Car roof (darker shade)
        roof_color = (180, 15, 50)
        pygame.draw.rect(self.screen, roof_color, 
                        (cx + 8, cy + 20, CAR_WIDTH - 16, 30), border_radius=4)
        
        # Front windshield with gradient effect
        windshield_color = (100, 180, 255)
        windshield_dark = (60, 120, 200)
        
        # Front windshield
        pygame.draw.polygon(self.screen, windshield_dark, [
            (cx + 8, cy + 8),
            (cx + 32, cy + 8),
            (cx + 28, cy + 22),
            (cx + 12, cy + 22)
        ])
        pygame.draw.polygon(self.screen, windshield_color, [
            (cx + 10, cy + 10),
            (cx + 30, cy + 10),
            (cx + 27, cy + 21),
            (cx + 13, cy + 21)
        ])
        
        # Rear windshield
        pygame.draw.polygon(self.screen, windshield_dark, [
            (cx + 12, cy + 48),
            (cx + 28, cy + 48),
            (cx + 32, cy + 62),
            (cx + 8, cy + 62)
        ])
        pygame.draw.polygon(self.screen, windshield_color, [
            (cx + 13, cy + 49),
            (cx + 27, cy + 49),
            (cx + 30, cy + 61),
            (cx + 10, cy + 61)
        ])
        
        # Headlights
        pygame.draw.ellipse(self.screen, (255, 255, 200), (cx + 6, cy + 2, 8, 5))
        pygame.draw.ellipse(self.screen, (255, 255, 200), (cx + 26, cy + 2, 8, 5))
        
        # Taillights
        pygame.draw.ellipse(self.screen, (255, 0, 0), (cx + 6, cy + 63, 8, 5))
        pygame.draw.ellipse(self.screen, (255, 0, 0), (cx + 26, cy + 63, 8, 5))
        
        # Side mirrors
        pygame.draw.rect(self.screen, (150, 150, 150), (cx - 2, cy + 28, 3, 6))
        pygame.draw.rect(self.screen, (150, 150, 150), (cx + 39, cy + 28, 3, 6))
        
        # Door lines
        pygame.draw.line(self.screen, (150, 20, 40), (cx + 8, cy + 25), (cx + 8, cy + 55), 1)
        pygame.draw.line(self.screen, (150, 20, 40), (cx + 32, cy + 25), (cx + 32, cy + 55), 1)
    
    def draw_ui(self):
        """Render score and game information."""
        # Score and overtakes
        score_text = self.font.render(f"Score: {self.score}", True, TEXT_COLOR)
        self.screen.blit(score_text, (20, 20))
        
        overtake_text = self.small_font.render(f"Overtakes: {self.overtakes}", True, TEXT_COLOR)
        self.screen.blit(overtake_text, (20, 60))
        
        # Speed indicator
        speed_text = self.small_font.render(f"Speed: {int(self.speed)}", True, TEXT_COLOR)
        self.screen.blit(speed_text, (20, 90))
        
        # Game over screen
        if self.game_over:
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            overlay.set_alpha(180)
            overlay.fill((0, 0, 0))
            self.screen.blit(overlay, (0, 0))
            
            game_over_text = self.font.render("CRASH!", True, (255, 50, 50))
            final_score_text = self.font.render(f"Final Score: {self.score}", True, TEXT_COLOR)
            overtakes_text = self.small_font.render(f"Total Overtakes: {self.overtakes}", True, TEXT_COLOR)
            restart_text = self.small_font.render("Press R to Restart or ESC to Quit", True, TEXT_COLOR)
            
            self.screen.blit(game_over_text, 
                           (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, 180))
            self.screen.blit(final_score_text, 
                           (SCREEN_WIDTH // 2 - final_score_text.get_width() // 2, 240))
            self.screen.blit(overtakes_text, 
                           (SCREEN_WIDTH // 2 - overtakes_text.get_width() // 2, 280))
            self.screen.blit(restart_text, 
                           (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, 340))
    
    def render(self):
        """Main rendering function."""
        self.draw_road()
        
        # Draw all traffic cars
        for car in self.traffic:
            car.draw(self.screen)
        
        self.draw_car()
        self.draw_ui()
        
        pygame.display.flip()
        self.clock.tick(60)  # 60 FPS
    
    def get_safe_spawn_lane(self):
        """
        Find a safe lane to spawn traffic that won't block all paths.
        Uses stricter checking to ensure player always has escape route.
        """
        # Check a larger danger zone at the top of screen
        DANGER_ZONE = 250  # Increased from 150
        
        # Get lanes that have traffic in the danger zone
        blocked_lanes = set()
        for car in self.traffic:
            if car.y < DANGER_ZONE:  # Car is in danger zone
                blocked_lanes.add(car.lane)
        
        # Get available safe lanes
        available_lanes = [i for i in range(LANE_COUNT) if i not in blocked_lanes]
        
        # If less than 2 lanes available, don't spawn (keep it safe)
        if len(available_lanes) < 2:
            return None  # Signal to skip spawning this time
        
        # Randomly choose from available safe lanes
        return random.choice(available_lanes)
    
    def should_spawn_traffic(self):
        """
        Additional check to prevent spawning when screen is too crowded.
        Returns True if it's safe to spawn new traffic.
        """
        # Count cars in upper half of screen
        cars_in_upper_half = sum(1 for car in self.traffic if car.y < SCREEN_HEIGHT // 2)
        
        # Don't spawn if too many cars already in upper area
        MAX_CARS_UPPER = 4
        return cars_in_upper_half < MAX_CARS_UPPER


# ============================================================
#                        Main Game Loop
# ============================================================

def main():
    """Main game loop."""
    game = HighwayGame()
    running = True
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            # Spawn traffic at regular intervals with safety checks
            if event.type == game.SPAWN_EVENT and not game.game_over:
                # Only spawn if it's safe to do so
                if game.should_spawn_traffic():
                    lane = game.get_safe_spawn_lane()
                    # Only spawn if we found a safe lane (not None)
                    if lane is not None:
                        game.traffic.append(TrafficCar(lane))
            
            # Keyboard events
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                
                # Restart game
                if event.key == pygame.K_r and game.game_over:
                    game.reset()
                
                # Handle lane changes
                if not game.game_over:
                    game.handle_lane_change(event)
        
        # Game logic
        if not game.game_over:
            game.handle_input()
        game.update()
        game.render()
    
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()