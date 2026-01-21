import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import math
import random

# --- KONFIGURASI ---
WINDOW_WIDTH = 1024
WINDOW_HEIGHT = 768
GAME_TITLE = "Jet Simulator 3D"
FPS = 60

# --- UTILS ---
def draw_text_on_screen(text_surface, x, y, window_width, window_height):
    text_data = pygame.image.tostring(text_surface, "RGBA", True)
    w, h = text_surface.get_size()
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    gluOrtho2D(0, window_width, 0, window_height)
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    glDisable(GL_DEPTH_TEST)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glRasterPos2i(x, window_height - y - h)
    glDrawPixels(w, h, GL_RGBA, GL_UNSIGNED_BYTE, text_data)
    glDisable(GL_BLEND)
    glEnable(GL_DEPTH_TEST)
    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)

# --- TEXTURE MANAGER ---
class TextureManager:
    textures = {}
    @staticmethod
    def generate_surface(width, height, type="noise"):
        surface = pygame.Surface((width, height))
        if type == "ground":
            surface.fill((30, 100, 30))
            for _ in range(5000): 
                surface.set_at((random.randint(0, width-1), random.randint(0, height-1)), (20, random.randint(80, 160), 20))
        elif type == "mountain":
            surface.fill((80, 80, 90))
            for _ in range(400): 
                surface.set_at((random.randint(0, width-1), random.randint(0, int(height/2.5))), (240, 240, 255))
        elif type == "cloud":
            surface.fill((200, 200, 200)) # Not used for primitive cloud but kept
            
        return surface

    @staticmethod
    def load_texture(name, surface):
        tex_id = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, tex_id)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, surface.get_width(), surface.get_height(), 0, GL_RGBA, GL_UNSIGNED_BYTE, pygame.image.tostring(surface, "RGBA", 1))
        TextureManager.textures[name] = tex_id
        return tex_id
        
    @staticmethod
    def get(name): return TextureManager.textures.get(name)
    
# --- SYSTEMS ---
class DayNightSystem:
    def __init__(self):
        self.state = "SIANG"
        self.timer = 0
        self.duration = 60000
        self.colors = {"SIANG": ((0.4, 0.7, 0.95, 1), (0.9, 0.9, 0.8, 1)), "SORE": ((0.8, 0.5, 0.2, 1), (0.8, 0.6, 0.3, 1)), "MALAM": ((0.05, 0.05, 0.1, 1), (0.2, 0.2, 0.35, 1))}
        self.sun_pos = [0, 100, 0, 0]
        self.current = self.colors["SIANG"]
        
    def update(self, dt):
        self.timer += dt
        cycle = self.timer % (self.duration * 3)
        if cycle < self.duration: 
            self.state, self.current, self.sun_pos = "SIANG", self.colors["SIANG"], [-50, 100, 50, 0]
        elif cycle < self.duration * 2: 
            self.state, self.current, self.sun_pos = "SORE", self.colors["SORE"], [-80, 20, 50, 0]
        else: 
            self.state, self.current, self.sun_pos = "MALAM", self.colors["MALAM"], [20, 80, -20, 0]
            
    def apply(self):
        glClearColor(*self.current[0])
        glLightfv(GL_LIGHT0, GL_POSITION, self.sun_pos)
        glLightfv(GL_LIGHT0, GL_DIFFUSE, self.current[1])
        glLightfv(GL_LIGHT0, GL_AMBIENT, [c * 0.4 for c in self.current[1]])

class AudioSystem:
    def __init__(self):
        try: 
            pygame.mixer.init()
            self.enabled = True
        except Exception as e: 
            print(f"Audio system disabled: {e}")
            self.enabled = False
        self.sounds = {}
        for n in ["engine", "wind", "crash"]: 
             pass
             
    def play(self, n): 
        if self.enabled and self.sounds.get(n): self.sounds[n].play()

# --- DRAWING ---
def draw_box(size, color=None, texture_name=None, repeat_x=1, repeat_y=1):
    x, y, z = size
    tex_id = TextureManager.get(texture_name) if texture_name else None
    
    if tex_id: 
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, tex_id)
        glColor3f(1,1,1)
    elif color: 
        glDisable(GL_TEXTURE_2D)
        glMaterialfv(GL_FRONT, GL_DIFFUSE, color + (1.0,))
        glColor3fv(color)
        
    verts = [( x, -y, -z), ( x,  y, -z), (-x,  y, -z), (-x, -y, -z), ( x, -y,  z), ( x,  y,  z), (-x,  y,  z), (-x, -y,  z)]
    uvs = [(0,0), (repeat_x,0), (repeat_x,repeat_y), (0,repeat_y)]
    faces = [(0,1,2,3), (4,5,6,7), (2,6,7,3), (0,4,5,1), (1,5,6,2), (0,3,7,4)]
    norms = [(0,0,-1), (0,0,1), (-1,0,0), (1,0,0), (0,1,0), (0,-1,0)]
    
    glBegin(GL_QUADS)
    for i, face in enumerate(faces):
        glNormal3fv(norms[i])
        for j, v_idx in enumerate(face):
            if tex_id: glTexCoord2f(uvs[j][0], uvs[j][1])
            glVertex3fv(verts[v_idx])
    glEnd()
    if tex_id: glDisable(GL_TEXTURE_2D)

def draw_pyramid_tex(size, tex, color):
    x, y, z = size
    tex_id = TextureManager.get(tex)
    if tex_id: 
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, tex_id)
        glColor3f(1,1,1)
    else: 
        glDisable(GL_TEXTURE_2D)
        glMaterialfv(GL_FRONT, GL_DIFFUSE, color + (1.0,))
        glColor3fv(color)
        
    glBegin(GL_TRIANGLES)
    norms = [(0,0.5,1), (1,0.5,0), (0,0.5,-1), (-1,0.5,0)]
    faces = [((0,y,0),(-x,-y,z),(x,-y,z)), ((0,y,0),(x,-y,z),(x,-y,-z)), ((0,y,0),(x,-y,-z),(-x,-y,-z)), ((0,y,0),(-x,-y,-z),(-x,-y,z))]
    t_coords = [(0.5,1), (0,0), (1,0)]
    
    for i, face in enumerate(faces):
        glNormal3f(*norms[i])
        for j, v in enumerate(face): 
            if tex_id: glTexCoord2f(*t_coords[j])
            glVertex3f(*v)
    glEnd()
    glDisable(GL_TEXTURE_2D)

def draw_plane_model(color_body, color_wing):
    # Fuselage
    glPushMatrix()
    glScalef(1.0, 0.8, 3.5)
    draw_box((0.5, 0.5, 0.5), color=color_body)
    glPopMatrix()
    
    # Wings
    glPushMatrix()
    glTranslatef(0, 0.2, 0.5)
    glScalef(4.0, 0.1, 0.8)
    draw_box((0.5, 0.5, 0.5), color=color_wing)
    glPopMatrix()
    
    # Tail H
    glPushMatrix()
    glTranslatef(0, 0.2, 1.5)
    glScalef(1.5, 0.1, 0.5)
    draw_box((0.5, 0.5, 0.5), color=color_wing)
    glPopMatrix()
    
    # Tail V
    glPushMatrix()
    glTranslatef(0, 0.8, 1.5)
    glScalef(0.1, 0.8, 0.5)
    draw_box((0.5, 0.5, 0.5), color=color_wing)
    glPopMatrix()
    
    # Propeller
    glPushMatrix()
    glTranslatef(0, 0, -1.8)
    glRotatef(pygame.time.get_ticks() % 360 * 5, 0, 0, 1) # Faster spin
    glScalef(1.2, 0.1, 0.1)
    draw_box((0.5, 0.5, 0.5), color=(0.2,0.2,0.2))
    glPopMatrix()

# --- GAME OBJECTS ---

class Bird:
    def __init__(self, z_start):
        self.x = random.uniform(-200, 200)
        self.y = random.uniform(50, 200)
        self.z = z_start
        self.wing_state = 0
        self.speed_z = random.uniform(0.5, 0.8)
        self.speed_x = random.uniform(-0.2, 0.2)
        
    def update(self):
        self.z += self.speed_z
        self.x += self.speed_x
        self.wing_state += 0.5
        
    def draw(self):
        glPushMatrix()
        glTranslatef(self.x, self.y, self.z)
        glRotatef(180, 0, 1, 0) # Face away from camera mostly (flying along with player?) or towards
        
        wing_y = math.sin(self.wing_state) * 0.5
        
        glColor3f(0.2, 0.2, 0.2)
        
        # Left wing
        glBegin(GL_TRIANGLES)
        glVertex3f(0, 0, 0)
        glVertex3f(-1.0, wing_y, 0.5)
        glVertex3f(0, 0, 1.0)
        glEnd()
        
        # Right wing
        glBegin(GL_TRIANGLES)
        glVertex3f(0, 0, 0)
        glVertex3f(1.0, wing_y, 0.5)
        glVertex3f(0, 0, 1.0)
        glEnd()
        
        glPopMatrix()

class EnemyPlane:
    def __init__(self, z_start):
        self.x = random.uniform(-100, 100)
        self.y = random.uniform(20, 150)
        self.z = z_start
        self.speed = random.uniform(0.8, 1.2)
        self.color_body = (random.random(), random.random(), random.random())
        self.color_wing = (random.random(), random.random(), random.random())
        self.rot_z = 0

    def update(self):
        self.z += self.speed 
        self.y += math.sin(self.z * 0.05) * 0.2
        self.rot_z = math.sin(self.z * 0.05) * 20

    def draw(self, is_night):
        glPushMatrix()
        glTranslatef(self.x, self.y, self.z)
        glRotatef(180, 0, 1, 0) 
        glRotatef(self.rot_z, 0, 0, 1)
        draw_plane_model(self.color_body, self.color_wing)
        glPopMatrix()

class Cloud:
    def __init__(self, z_start):
        self.x = random.randint(-500, 500)
        self.y = random.randint(100, 300)
        self.z = z_start
        self.components = []
        # Generate varied cloud shape
        for _ in range(random.randint(3, 6)):
            off_x = random.uniform(-15, 15)
            off_y = random.uniform(-5, 5)
            off_z = random.uniform(-10, 10)
            sz = random.uniform(8, 20)
            self.components.append((off_x, off_y, off_z, sz))
            
    def draw(self):
        glPushMatrix()
        glTranslatef(self.x, self.y, self.z)
        for c in self.components:
            glPushMatrix()
            glTranslatef(c[0], c[1], c[2])
            glScalef(c[3], c[3]*0.6, c[3])
            draw_box((1,1,1), color=(0.95, 0.95, 1.0)) 
            glPopMatrix()
        glPopMatrix()

class PlayerPlane:
    def __init__(self, audio):
        self.audio = audio
        self.x = 0
        self.y = 100
        self.z = 0
        self.vel_x = 0
        self.vel_y = 0
        self.vel_z = -9.5 # Much Faster
        self.bank = 0
        self.pitch = 0
        self.crashed = False
        
    def update(self, keys):
        if self.crashed: 
            self.y -= 2.0 
            self.z += self.vel_z * 0.5
            self.bank += 10
            return

        target_bank = 0
        target_pitch = 0
        
        if keys[K_w]: target_pitch = 30; self.vel_y = 0.8
        elif keys[K_s]: target_pitch = -30; self.vel_y = -0.8
        else: self.vel_y = 0 

        if keys[K_a]: target_bank = 60; self.vel_x = -1.2
        elif keys[K_d]: target_bank = -60; self.vel_x = 1.2
        else: self.vel_x = 0

        self.bank += (target_bank - self.bank) * 0.08
        self.pitch += (target_pitch - self.pitch) * 0.08
        self.x += self.vel_x
        self.y += self.vel_y
        self.z += self.vel_z
        
        # Ground collision hard limit
        if self.y < 5:
            self.crashed = True
            
        self.x = max(-450, min(450, self.x))
        self.y = max(5, min(400, self.y))

    def draw(self, is_night):
        glPushMatrix()
        glTranslatef(self.x, self.y, self.z)
        glRotatef(self.pitch, 1, 0, 0)
        glRotatef(self.bank, 0, 0, 1)
        
        draw_plane_model((0.8, 0.2, 0.2), (0.9, 0.9, 0.9))
        
        if is_night:
            glPushMatrix(); glTranslatef(3.5, 0, 0.5); glScalef(0.1,0.1,0.1); glMaterialfv(GL_FRONT, GL_EMISSION, (0,1,0,1)); draw_box((1,1,1), color=(0,1,0)); glPopMatrix()
            glPushMatrix(); glTranslatef(-3.5, 0, 0.5); glScalef(0.1,0.1,0.1); glMaterialfv(GL_FRONT, GL_EMISSION, (1,0,0,1)); draw_box((1,1,1), color=(1,0,0)); glPopMatrix()
            glMaterialfv(GL_FRONT, GL_EMISSION, (0,0,0,1))
            
        glPopMatrix()

class Environment:
    def draw(self, player_z, is_night):
        sl = 400; cs = int(player_z // sl)
        tex_ground = TextureManager.get("ground")
        tex_mtn = TextureManager.get("mountain")
        
        for i in range(cs - 2, cs + 3):
            z_s = i * sl
            glPushMatrix()
            glTranslatef(0, -10, z_s) # Lower ground slightly to give more room
            glScalef(200, 1, sl/2)
            draw_box((1,1,1), texture_name="ground", repeat_x=10, repeat_y=10)
            glPopMatrix()
            
            random.seed(i)
            for _ in range(8):
                mx = random.choice([-1, 1]) * random.randint(150, 500)
                glPushMatrix()
                glTranslatef(mx, random.randint(30, 100), random.randint(0, int(sl)))
                glScalef(random.uniform(2,4), random.uniform(2,5), random.uniform(2,4))
                draw_pyramid_tex((50,100,50), "mountain", (0.4, 0.4, 0.5))
                glPopMatrix()

class Camera:
    def __init__(self):
        self.distance = 45.0
        self.angle_y = 0.0
        self.angle_x = 20.0
        self.is_dragging = False
        self.last_pos = (0, 0)
        self.roll = 0
        
    def process_event(self, event):
        if event.type == MOUSEBUTTONDOWN:
            if event.button == 1:
                self.is_dragging = True
                self.last_pos = pygame.mouse.get_pos()
            elif event.button == 4:
                self.distance = max(20.0, self.distance - 2.0)
            elif event.button == 5:
                self.distance = min(120.0, self.distance + 2.0)
        elif event.type == MOUSEBUTTONUP:
            if event.button == 1:
                self.is_dragging = False
        elif event.type == MOUSEMOTION:
            if self.is_dragging:
                mx, my = pygame.mouse.get_pos()
                dx = mx - self.last_pos[0]
                dy = my - self.last_pos[1]
                self.last_pos = (mx, my)
                self.angle_y += dx * 0.5
                self.angle_x += dy * 0.5
                self.angle_x = max(-60, min(80, self.angle_x)) 

    def apply(self, target_pos, target_bank):
        rad_y = math.radians(self.angle_y)
        rad_x = math.radians(self.angle_x)
        
        dist_h = self.distance * math.cos(rad_x)
        y_cam = self.distance * math.sin(rad_x)
        x_cam = dist_h * math.sin(rad_y)
        z_cam = dist_h * math.cos(rad_y)
        
        # Add dynamic bank to camera
        self.roll += (target_bank * 0.5 - self.roll) * 0.1 # Smooth roll follow
        
        # Apply transforms manually for Camera Roll
        # The lookAt is standard, but we need to rotate the whole scene logic OR use gluLookAt up vector
        # Using Up-Vector for banking:
        # Standard Up is (0,1,0). Rotated Up around Z-axis (forward)
        
        up_x = math.sin(math.radians(-self.roll))
        up_y = math.cos(math.radians(-self.roll))
        
        gluLookAt(target_pos[0] + x_cam, target_pos[1] + y_cam, target_pos[2] + z_cam, 
                  target_pos[0], target_pos[1], target_pos[2], 
                  up_x, up_y, 0)

# --- MAIN ---
def main():
    pygame.init(); pygame.font.init()
    display = (WINDOW_WIDTH, WINDOW_HEIGHT)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    pygame.display.set_caption(GAME_TITLE)
    font = pygame.font.SysFont("Arial", 24)
    
    glViewport(0, 0, *display)
    glMatrixMode(GL_PROJECTION); glLoadIdentity(); gluPerspective(60, (display[0]/display[1]), 0.1, 2500.0)
    glMatrixMode(GL_MODELVIEW); glLoadIdentity()
    glEnable(GL_DEPTH_TEST); glEnable(GL_LIGHTING); glEnable(GL_LIGHT0); glEnable(GL_COLOR_MATERIAL)
    glEnable(GL_NORMALIZE)
    
    TextureManager.load_texture("ground", TextureManager.generate_surface(512, 512, "ground"))
    TextureManager.load_texture("mountain", TextureManager.generate_surface(256, 256, "mountain"))
    
    dn = DayNightSystem(); aud = AudioSystem(); 
    player = PlayerPlane(aud)
    env = Environment()
    cam = Camera()
    
    enemies = []
    clouds = []
    birds = []
    
    next_spawn_z = -200
    next_cloud_z = -100
    next_bird_z = -300
    
    clk = pygame.time.Clock(); run = True; msg = ""
    
    # Pre-populate clouds
    for i in range(20):
        clouds.append(Cloud(random.randint(-1000, 0)))
    
    while run:
        dt = clk.tick(FPS)
        for e in pygame.event.get(): 
            if e.type == QUIT or (e.type == KEYDOWN and e.key == K_ESCAPE): run = False
            if player.crashed and e.type == KEYDOWN and e.key == K_r:
                player = PlayerPlane(aud); enemies = []; clouds = []; birds = []; next_spawn_z = player.z - 200
            cam.process_event(e)
        
        dn.update(dt)
        player.update(pygame.key.get_pressed())
        
        # Spawning Logic
        if player.z < next_spawn_z + 300:
            enemies.append(EnemyPlane(next_spawn_z - 400))
            next_spawn_z -= random.randint(300, 700)
            
        if player.z < next_cloud_z + 200:
            clouds.append(Cloud(next_cloud_z - 400))
            next_cloud_z -= random.randint(100, 250)
            
        if player.z < next_bird_z + 500:
            for _ in range(random.randint(3, 7)): # Flock
                birds.append(Bird(next_bird_z - 400 + random.uniform(-20, 20)))
            next_bird_z -= random.randint(500, 1000)
            
        # Logic Loop
        if not player.crashed:
            for e in enemies: e.update()
            for b in birds: b.update()
            
            # Crash Checks
            for e in enemies:
                if abs(player.z - e.z) < 5.0 and abs(player.x - e.x) < 5.0 and abs(player.y - e.y) < 5.0:
                    player.crashed = True; msg = "MID-AIR COLLISION!"
                    
            for b in birds:
                if abs(player.z - b.z) < 2.0 and abs(player.x - b.x) < 2.0 and abs(player.y - b.y) < 2.0:
                    player.crashed = True; msg = "BIRD STRIKE!"

        dn.apply()
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        
        cam.apply((player.x, player.y, player.z), player.bank)
        
        is_n = dn.state == "MALAM"
        env.draw(player.z, is_n)
        
        for c in clouds: c.draw()
        for e in enemies: e.draw(is_n)
        for b in birds: b.draw()
        
        player.draw(is_n)

        # UI
        draw_text_on_screen(font.render(f"ALT: {int(player.y)} ft", True, (255,255,255)), 20, 20, WINDOW_WIDTH, WINDOW_HEIGHT)
        draw_text_on_screen(font.render(f"TIME: {dn.state}", True, (255,255,255)), 800, 20, WINDOW_WIDTH, WINDOW_HEIGHT)
        
        if player.crashed:
            draw_text_on_screen(font.render("CRASHED! PRESS 'R' TO RESTART", True, (255,0,0)), 350, 384, WINDOW_WIDTH, WINDOW_HEIGHT)
            if msg: draw_text_on_screen(font.render(msg, True, (255,255,0)), 400, 350, WINDOW_WIDTH, WINDOW_HEIGHT)
            
        pygame.display.flip()
        
        # Cleanup
        if len(enemies) > 20: enemies.pop(0)
        if len(clouds) > 40: clouds.pop(0)
        if len(birds) > 50: birds.pop(0)

    pygame.quit()

if __name__ == "__main__": main()