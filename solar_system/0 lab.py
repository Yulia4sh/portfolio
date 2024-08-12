import wx
import pygame
from math import sqrt, atan2, cos, sin, log2
import time
import random


class Planet:

    a_o = 149.6e6*1000
    G = 6.67428e-11
    dt = 60*60*24*2
    scale = 100/a_o

    def __init__(self, x, y, radius, img, mass, angle):
        self.x = x
        self.y = y
        self.radius = radius
        self.img = img
        self.mass = mass
        self.angle = angle
        self.angle_iter = 0
        self.x_vel = 0
        self.y_vel = 0
        self.orbit = []
        self.sun = False
        self.moon = False
        self.dist_to_sun = 0
        self.force = 0
        self.dx_a = self.dy_a = 0

    def draw(self, window):
        W, H = pygame.display.Info().current_w, pygame.display.Info().current_h
        x = self.x*self.scale+W/2
        y = self.y*self.scale+H/2
        if len(self.orbit) > 2:
            updated_points = []
            for point in self.orbit:
                x, y = point
                x = x*self.scale+W/2
                y = y*self.scale+H/2
                updated_points.append((x, y))
        load_img = pygame.image.load(self.img)
        load_img = pygame.transform.scale(load_img, (self.radius*2, self.radius*2))
        load_img = pygame.transform.rotate(load_img, self.angle_iter)
        self.angle_iter += self.angle
        if self.angle_iter >= 360:
            self.angle_iter = 0
        self.load_img_rect = load_img.get_rect(center=(x, y))
        window.blit(load_img, self.load_img_rect)

    def attraction(self, local, other):
        other_x, other_y = other.x, other.y
        if local.moon:
            dx, dy = other.orbit[-1]
            try:
                dx, dy = dx - other.orbit[-2][0], dy-other.orbit[-2][1]
            except IndexError:
                dx, dy = 0, 0
            local.x += dx
            local.y += dy
        distance_x = other_x-local.x
        distance_y = other_y-local.y
        distance = sqrt(distance_x**2+distance_y**2)
        if other.sun:
            local.dist_to_sun = distance
        self.force = local.G*local.mass*other.mass/distance**2
        if local.moon:
            self.force *= 10**3.75
        theta = atan2(distance_y, distance_x)
        force_x = self.force*cos(theta)
        force_y = self.force*sin(theta)
        return force_x, force_y

    def update_position(self, planet):
        total_fx = total_fy = 0
        if self.sun:
            self.orbit.append((self.x, self.y))
            return
        force_x, force_y = self.attraction(self, planet)
        total_fx += force_x
        total_fy += force_y
        self.x_vel += total_fx/self.mass*self.dt
        self.y_vel += total_fy/self.mass*self.dt
        self.x += self.x_vel*self.dt
        self.y += self.y_vel*self.dt
        self.orbit.append((self.x, self.y))

    def update_scale_minus(self, scale):
        self.radius *= scale

    def update_scale_plus(self, scale):
        self.radius /= scale

    def draw_asteroid(self, x, y, window):
        load_img = pygame.image.load('asteroid.png')
        load_img = pygame.transform.scale(load_img, (self.radius * 2, self.radius * 2))
        self.load_img_rect = load_img.get_rect(center=(x, y))
        window.blit(load_img, self.load_img_rect)

    def update_asteroid(self):
        dx = self.x - pygame.mouse.get_pos()[0]
        dy = self.y - pygame.mouse.get_pos()[1]
        angle = atan2(dy, dx)
        self.x += self.y_vel * cos(angle)
        self.y += self.y_vel * sin(angle)

    def collide(self, planets):
        planeta = False
        colide = False
        for planet in planets:
            if self.load_img_rect.colliderect(planet.load_img_rect):
                planeta = planet
        if planeta != False:
            colide = True

        return colide, planeta



class MainPygame:
    def __init__(self, m_mercury, v_mercury, r_mercury, t_mercury,
         m_venus, v_venus, r_venus, t_venus,
         m_earth, v_earth, r_earth, t_earth,
         m_mars, v_mars, r_mars, t_mars,
         m_jupiter, v_jupiter, r_jupiter, t_jupiter,
         m_saturn, v_saturn, r_saturn, t_saturn,
         m_uranus, v_uranus, r_uranus, t_uranus,
         m_neptune, v_neptune, r_neptune, t_neptune,
         m_moon, v_moon, r_moon, t_moon,
         m_sun, v_sun, r_sun, t_sun,
         parent,
         m_asteroid, v_asteroid, r_asteroid, t_asteroid):

        self.m_mercury = m_mercury if m_mercury is not None else 3.2 * 10 ** 23
        self.v_mercury = v_mercury if v_mercury is not None else 47.4
        self.r_mercury = log2(r_mercury) if r_mercury is not None else 5
        self.t_mercury = t_mercury if t_mercury is not None else 58

        self.m_venus = m_venus if m_venus is not None else 4.8 * 10 ** 24
        self.v_venus = v_venus if v_venus is not None else 35.02
        self.r_venus = log2(r_venus) if r_venus is not None else 9
        self.t_venus = t_venus if t_venus is not None else 243

        self.m_earth = m_earth if m_earth is not None else 5.9 * 10 ** 24
        self.v_earth = v_earth if v_earth is not None else 29.783
        self.r_earth = log2(r_earth) if r_earth is not None else 10
        self.t_earth = t_earth if t_earth is not None else 1

        self.m_mars = m_mars if m_mars is not None else 6.39 * 10 ** 23
        self.v_mars = v_mars if v_mars is not None else 24.077
        self.r_mars = log2(r_mars) if r_mars is not None else 5
        self.t_mars = t_mars if t_mars is not None else 24.6

        self.m_jupiter = m_jupiter if m_jupiter is not None else 1.89 * 10 ** 27
        self.v_jupiter = v_jupiter if v_jupiter is not None else 13.06
        self.r_jupiter = log2(r_jupiter) if r_jupiter is not None else 20
        self.t_jupiter = t_jupiter if t_jupiter is not None else 9

        self.m_saturn = m_saturn if m_saturn is not None else 5.68 * 10 ** 26
        self.v_saturn = v_saturn if v_saturn is not None else 9.68
        self.r_saturn = log2(r_saturn) if r_saturn is not None else 18
        self.t_saturn = t_saturn if t_saturn is not None else 10

        self.m_uranus = m_uranus if m_uranus is not None else 6.68 * 10 ** 25
        self.v_uranus = v_uranus if v_uranus is not None else 6.80
        self.r_uranus = log2(r_uranus) if r_uranus is not None else 14
        self.t_uranus = t_uranus if t_uranus is not None else 17

        self.m_neptune = m_neptune if m_neptune is not None else 1.02 * 10 ** 26
        self.v_neptune = v_neptune if v_neptune is not None else 5.43
        self.r_neptune = log2(r_neptune) if r_neptune is not None else 12
        self.t_neptune = t_neptune if t_neptune is not None else 16

        self.m_moon = m_moon if m_moon is not None else 7.3 * 10 ** 22
        self.v_moon = v_moon if v_moon is not None else 7
        self.r_moon = log2(r_moon) if r_moon is not None else 5
        self.t_moon = t_moon if t_moon is not None else 27

        self.m_sun = m_sun if m_sun is not None else 1.9*10**30
        self.v_sun = v_sun if v_sun is not None else 0
        self.r_sun = log2(r_sun) if r_sun is not None else 30
        self.t_sun = t_sun if t_sun is not None else 1

        self.m_asteroid = m_asteroid if m_asteroid is not None else 10**4
        self.v_asteroid = v_asteroid if v_asteroid is not None else 3
        self.r_asteroid = log2(r_asteroid) if r_asteroid is not None else 25
        self.t_asteroid = t_asteroid if t_asteroid is not None else 0.5

        pygame.init()
        sc = pygame.display.set_mode((1366, 768))

        run = True
        clock = pygame.time.Clock()
        self.sun = Planet(0, 0, self.r_sun*Planet.scale*10**9, "sun.png", self.m_sun, self.t_sun)
        self.sun.sun = True
        self.mercury = Planet(-0.387*Planet.a_o, 0, self.r_mercury*Planet.scale*10**9, "mercury.png", self.m_mercury, self.t_mercury*24)
        self.mercury.y_vel = self.v_mercury*1000
        self.venus = Planet(-0.723*Planet.a_o, 0, self.r_venus*Planet.scale*10**9, "venus.png", self.m_venus, self.t_venus*24)
        self.venus.y_vel = self.v_venus*1000
        self.earth = Planet(-1*Planet.a_o, 0, self.r_earth*Planet.scale*10**9, "earth.png", self.m_earth, self.t_earth*24)
        self.earth.y_vel = self.v_earth*1000
        self.mars = Planet(-1.524*Planet.a_o, 0, self.r_mars*Planet.scale*10**9, "mars.png", self.m_mars, self.t_mars)
        self.mars.y_vel = self.v_mars*1000
        self.jupiter = Planet(-5.204*Planet.a_o, 0, self.r_jupiter*Planet.scale*10**9, "jupiter.png", self.m_jupiter, self.t_jupiter)
        self.jupiter.y_vel = self.v_jupiter*1000
        self.saturn = Planet(-9.573*Planet.a_o, 0, self.r_saturn*Planet.scale*10**9, "saturn.png", self.m_saturn, self.t_saturn)
        self.saturn.y_vel = self.v_saturn*1000
        self.uranus = Planet(-19.165*Planet.a_o, 0, self.r_uranus*Planet.scale*10**9, "uranus.png", self.m_uranus, self.t_uranus)
        self.uranus.y_vel = self.v_uranus*1000
        self.neptune = Planet(-30.178*Planet.a_o, 0, self.r_neptune*Planet.scale*10**9, "neptune.png", self.m_neptune, self.t_neptune)
        self.neptune.y_vel = self.v_neptune*1000
        self.moon = Planet(-1.2*Planet.a_o, 0, self.r_moon*Planet.scale*10**9, "moon.png", self.m_moon, self.t_moon*24)
        self.moon.y_vel = self.v_moon*1000
        self.moon.moon = True

        planets = [self.neptune, self.uranus, self.saturn, self.jupiter, self.mars, self.earth, self.venus, self.mercury, self.sun]
        bg = pygame.image.load("background.jpg")
        self.asteroid_this = True
        self.asteroid = Planet(random.randint(0, 1366), random.randint(0, 768),
                               self.r_asteroid * Planet.scale * 10 ** 9, "asteroid.png",
                               self.m_asteroid, self.t_asteroid * 24)
        self.asteroid.y_vel = -self.v_asteroid
        while run:
            clock.tick(60)
            sc.blit(bg, (0, 0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and (event.key == pygame.K_x or event.key ==
                                                                                   pygame.K_ESCAPE)):
                    run = False
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_MINUS:
                    for obj_system in [self.sun, self.mercury, self.venus, self.earth, self.mars, self.jupiter, self.saturn, self.uranus, self.neptune, self.moon]:
                        obj_system.scale *= 0.75
                        obj_system.update_scale_minus(0.75)
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    for obj_system in [self.sun, self.mercury, self.venus, self.earth, self.mars, self.jupiter, self.saturn, self.uranus, self.neptune, self.moon]:
                        obj_system.scale /= 0.75
                        obj_system.update_scale_plus(0.75)
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_TAB:
                    time.sleep(0.1)
                    parent.text = wx.StaticText(parent, label=f"{self.mercury.x}"[0:14], style=wx.ALIGN_CENTER,
                                                pos=(75, 109))
                    parent.text.SetForegroundColour(wx.WHITE)
                    parent.text = wx.StaticText(parent, label=f"{self.mercury.y}"[0:14], style=wx.ALIGN_CENTER,
                                                pos=(245, 109))
                    parent.text.SetForegroundColour(wx.WHITE)
                    parent.text = wx.StaticText(parent, label=f"{round(self.mercury.force)}", style=wx.ALIGN_CENTER,
                                                pos=(125, 69))
                    parent.text.SetForegroundColour(wx.WHITE)

                    parent.text = wx.StaticText(parent, label=f"{self.venus.x}"[0:14], style=wx.ALIGN_CENTER,
                                                pos=(75+320, 109))
                    parent.text.SetForegroundColour(wx.WHITE)
                    parent.text = wx.StaticText(parent, label=f"{self.venus.y}"[0:14], style=wx.ALIGN_CENTER,
                                                pos=(245+320, 109))
                    parent.text.SetForegroundColour(wx.WHITE)
                    parent.text = wx.StaticText(parent, label=f"{round(self.venus.force)}", style=wx.ALIGN_CENTER,
                                                pos=(125+320, 69))
                    parent.text.SetForegroundColour(wx.WHITE)

                    parent.text = wx.StaticText(parent, label=f"{self.earth.x}"[0:14], style=wx.ALIGN_CENTER,
                                                pos=(75 + 2*320, 101))
                    parent.text.SetForegroundColour(wx.WHITE)
                    parent.text = wx.StaticText(parent, label=f"{self.earth.y}"[0:14], style=wx.ALIGN_CENTER,
                                                pos=(245 + 2*320, 101))
                    parent.text.SetForegroundColour(wx.WHITE)
                    parent.text = wx.StaticText(parent, label=f"{round(self.earth.force)}", style=wx.ALIGN_CENTER,
                                                pos=(125 + 2*320, 69))
                    parent.text.SetForegroundColour(wx.WHITE)

                    parent.text = wx.StaticText(parent, label=f"{self.mars.x}"[0:14], style=wx.ALIGN_CENTER,
                                                pos=(75 + 3 * 332, 101+6))
                    parent.text.SetForegroundColour(wx.WHITE)
                    parent.text = wx.StaticText(parent, label=f"{self.mars.y}"[0:14], style=wx.ALIGN_CENTER,
                                                pos=(245 + 3 * 332, 101+6))
                    parent.text.SetForegroundColour(wx.WHITE)
                    parent.text = wx.StaticText(parent, label=f"{round(self.mars.force)}", style=wx.ALIGN_CENTER,
                                                pos=(125 + 3 * 332, 69))
                    parent.text.SetForegroundColour(wx.WHITE)

                    parent.text = wx.StaticText(parent, label=f"{self.jupiter.x}"[0:14], style=wx.ALIGN_CENTER,
                                                pos=(75, 109+380))
                    parent.text.SetForegroundColour(wx.WHITE)
                    parent.text = wx.StaticText(parent, label=f"{self.jupiter.y}"[0:14], style=wx.ALIGN_CENTER,
                                                pos=(245, 109+380))
                    parent.text.SetForegroundColour(wx.WHITE)
                    parent.text = wx.StaticText(parent, label=f"{round(self.jupiter.force)}", style=wx.ALIGN_CENTER,
                                                pos=(125, 69+390))
                    parent.text.SetForegroundColour(wx.WHITE)

                    parent.text = wx.StaticText(parent, label=f"{self.saturn.x}"[0:14], style=wx.ALIGN_CENTER,
                                                pos=(75 + 320, 109+380))
                    parent.text.SetForegroundColour(wx.WHITE)
                    parent.text = wx.StaticText(parent, label=f"{self.saturn.y}"[0:14], style=wx.ALIGN_CENTER,
                                                pos=(245 + 320, 109+380))
                    parent.text.SetForegroundColour(wx.WHITE)
                    parent.text = wx.StaticText(parent, label=f"{round(self.saturn.force)}", style=wx.ALIGN_CENTER,
                                                pos=(125 + 320, 69+390))
                    parent.text.SetForegroundColour(wx.WHITE)

                    parent.text = wx.StaticText(parent, label=f"{self.uranus.x}"[0:14], style=wx.ALIGN_CENTER,
                                                pos=(75 + 2 * 320, 101+395))
                    parent.text.SetForegroundColour(wx.WHITE)
                    parent.text = wx.StaticText(parent, label=f"{self.uranus.y}"[0:14], style=wx.ALIGN_CENTER,
                                                pos=(245 + 2 * 320, 101+395))
                    parent.text.SetForegroundColour(wx.WHITE)
                    parent.text = wx.StaticText(parent, label=f"{round(self.uranus.force)}", style=wx.ALIGN_CENTER,
                                                pos=(125 + 2 * 320, 69+390))
                    parent.text.SetForegroundColour(wx.WHITE)

                    parent.text = wx.StaticText(parent, label=f"{self.neptune.x}"[0:14], style=wx.ALIGN_CENTER,
                                                pos=(75 + 3 * 332, 101 + 6+390))
                    parent.text.SetForegroundColour(wx.WHITE)
                    parent.text = wx.StaticText(parent, label=f"{self.neptune.y}"[0:14], style=wx.ALIGN_CENTER,
                                                pos=(245 + 3 * 327, 101 + 6+390))
                    parent.text.SetForegroundColour(wx.WHITE)
                    parent.text = wx.StaticText(parent, label=f"{round(self.neptune.force)}", style=wx.ALIGN_CENTER,
                                                pos=(125 + 3 * 329, 69+390))
                    parent.text.SetForegroundColour(wx.WHITE)

                    parent.text = wx.StaticText(parent, label=f"{self.moon.x}"[0:14], style=wx.ALIGN_CENTER,
                                                pos=(75 + 2 * 320+180, 101-50))
                    parent.text.SetForegroundColour(wx.WHITE)
                    parent.text = wx.StaticText(parent, label=f"{self.moon.y}"[0:14], style=wx.ALIGN_CENTER,
                                                pos=(245 + 2 * 320+120, 101-50))
                    parent.text.SetForegroundColour(wx.WHITE)
                    parent.text = wx.StaticText(parent, label=f"{round(self.moon.force)}", style=wx.ALIGN_CENTER,
                                                pos=(125 + 2 * 320+168, 69-50+10))
                    parent.text.SetForegroundColour(wx.WHITE)

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.asteroid_this = True
                    self.asteroid = Planet(random.randint(0, 1366), random.randint(0, 768), self.r_asteroid * Planet.scale * 10 ** 9, "asteroid.png",
                                       self.m_asteroid, self.t_asteroid * 24)
                    self.asteroid.y_vel = -self.v_asteroid

                elif event.type == pygame.KEYDOWN and event.key == pygame.K_w and self.asteroid_this:
                    self.asteroid.radius += 5
                    self.asteroid.mass *= 10

                elif event.type == pygame.KEYDOWN and event.key == pygame.K_s and self.asteroid_this:
                    self.asteroid.radius -= 5
                    self.asteroid.mass /= 10

                elif event.type == pygame.KEYDOWN and event.key == pygame.K_d and self.asteroid_this:
                    self.asteroid.y_vel += 1

                elif event.type == pygame.KEYDOWN and event.key == pygame.K_a and self.asteroid_this:
                    self.asteroid.y_vel -= 1

            for planet in planets:
                planet.update_position(self.sun)
                planet.draw(sc)
            self.moon.update_position(self.earth)
            self.moon.draw(sc)


            if self.asteroid_this:
                self.asteroid.update_asteroid()
                self.asteroid.draw_asteroid(self.asteroid.x, self.asteroid.y, sc)
                collide, planet = self.asteroid.collide([self.sun, self.mercury, self.venus, self.earth, self.mars,self.jupiter, self.saturn, self.uranus, self.neptune, self.moon])
                if collide:
                    elastic = 1
                    planet.mass += self.asteroid.mass
                    before_y = planet.y_vel
                    planet.x_vel = (elastic * (self.asteroid.y_vel - planet.x_vel) + self.asteroid.mass * self.asteroid.y_vel + planet.mass * planet.x_vel) / (planet.mass + self.asteroid.mass)
                    planet.y_vel = (elastic * (self.asteroid.y_vel - planet.y_vel) + self.asteroid.mass * self.asteroid.y_vel + planet.mass * planet.y_vel) / (planet.mass + self.asteroid.mass)
                    self.asteroid.y_vel = -elastic * self.asteroid.y_vel

                    self.asteroid.update_asteroid()
                    self.asteroid.draw_asteroid(self.asteroid.x, self.asteroid.y, sc)

                    load_img = pygame.image.load('boom.png')
                    load_img_rect = planet.load_img_rect
                    load_img = pygame.transform.scale(load_img, (100, 100))
                    sc.blit(load_img, load_img_rect)
                    pygame.display.update()
                    load_img = pygame.transform.scale(load_img, (80, 80))
                    sc.blit(load_img, load_img_rect)

            font = pygame.font.Font(None, 36)
            text = [
                ("K_MINUS: Decrease the scale of all celestial objects.", (10, 10)),
                ("K_SPACE: Increase the scale of all celestial objects.", (10, 50)),
                ("K_TAB: Display information about the celestial objects using wxPython.", (10, 90)),
                ("K_w: Increase the radius and mass of the asteroid if it's present.", (10, 130)),
                ("K_s: Decrease the radius and mass of the asteroid if it's present.", (10, 170)),
                ("K_d: Increase the velocity of the asteroid if it's present.", (10, 210)),
                ("K_a: Decrease the velocity of the asteroid if it's present.", (10, 250)),
                ("Mouse Click: Create a new asteroid at a random position.", (10, 290))
            ]

            for msg, pos in text:
                label = font.render(msg, True, (255, 255, 255))
                sc.blit(label, pos)

            pygame.display.update()

        pygame.quit()


class MyPanel(wx.Panel):

    def __init__(self, parent):
        wx.Panel.__init__(self, parent)

        self.m_mercury = wx.TextCtrl(self, pos=(63, 303), size=(70, 20))
        self.v_mercury = wx.TextCtrl(self, pos=(190, 303), size=(70, 20))
        self.r_mercury = wx.TextCtrl(self, pos=(63, 326), size=(70, 20))
        self.t_mercury = wx.TextCtrl(self, pos=(190, 326), size=(70, 20))

        self.m_venus = wx.TextCtrl(self, pos=(413, 303), size=(70, 20))
        self.v_venus = wx.TextCtrl(self, pos=(540, 303), size=(70, 20))
        self.r_venus = wx.TextCtrl(self, pos=(413, 326), size=(70, 20))
        self.t_venus = wx.TextCtrl(self, pos=(540, 326), size=(70, 20))

        self.m_earth = wx.TextCtrl(self, pos=(733, 303), size=(70, 20))
        self.v_earth = wx.TextCtrl(self, pos=(850, 303), size=(70, 20))
        self.r_earth = wx.TextCtrl(self, pos=(733, 326), size=(70, 20))
        self.t_earth = wx.TextCtrl(self, pos=(850, 326), size=(70, 20))

        self.m_mars = wx.TextCtrl(self, pos=(1075, 303), size=(70, 20))
        self.v_mars = wx.TextCtrl(self, pos=(1205, 303), size=(70, 20))
        self.r_mars = wx.TextCtrl(self, pos=(1075, 326), size=(70, 20))
        self.t_mars = wx.TextCtrl(self, pos=(1205, 326), size=(70, 20))

        self.m_jupiter = wx.TextCtrl(self, pos=(63, 688), size=(70, 20))
        self.v_jupiter = wx.TextCtrl(self, pos=(190, 688), size=(70, 20))
        self.r_jupiter = wx.TextCtrl(self, pos=(63, 711), size=(70, 20))
        self.t_jupiter = wx.TextCtrl(self, pos=(190, 711), size=(70, 20))

        self.m_saturn = wx.TextCtrl(self, pos=(413, 688), size=(70, 20))
        self.v_saturn = wx.TextCtrl(self, pos=(540, 688), size=(70, 20))
        self.r_saturn = wx.TextCtrl(self, pos=(413, 711), size=(70, 20))
        self.t_saturn = wx.TextCtrl(self, pos=(540, 711), size=(70, 20))

        self.m_uranus = wx.TextCtrl(self, pos=(733, 688), size=(70, 20))
        self.v_uranus = wx.TextCtrl(self, pos=(850, 688), size=(70, 20))
        self.r_uranus = wx.TextCtrl(self, pos=(733, 711), size=(70, 20))
        self.t_uranus = wx.TextCtrl(self, pos=(850, 711), size=(70, 20))

        self.m_neptune = wx.TextCtrl(self, pos=(1075, 688), size=(70, 20))
        self.v_neptune = wx.TextCtrl(self, pos=(1205, 688), size=(70, 20))
        self.r_neptune = wx.TextCtrl(self, pos=(1075, 711), size=(70, 20))
        self.t_neptune = wx.TextCtrl(self, pos=(1205, 711), size=(70, 20))

        self.m_moon = wx.TextCtrl(self, pos=(913, 153), size=(40, 15))
        self.v_moon = wx.TextCtrl(self, pos=(1010, 153), size=(40, 15))
        self.r_moon = wx.TextCtrl(self, pos=(913, 170), size=(40, 15))
        self.t_moon = wx.TextCtrl(self, pos=(1010, 170), size=(40, 15))

        self.m_sun = wx.TextCtrl(self, pos=(1283, 238), size=(40, 15))
        self.v_sun = wx.TextCtrl(self, pos=(1388, 238), size=(40, 15))
        self.r_sun = wx.TextCtrl(self, pos=(1283, 255), size=(40, 15))
        self.t_sun = wx.TextCtrl(self, pos=(1388, 255), size=(40, 15))

        self.m_asteroid = wx.TextCtrl(self, pos=(255, 368), size=(40, 15))
        self.v_asteroid = wx.TextCtrl(self, pos=(350, 368), size=(40, 15))
        self.r_asteroid = wx.TextCtrl(self, pos=(255, 385), size=(40, 15))
        self.t_asteroid = wx.TextCtrl(self, pos=(350, 385), size=(40, 15))

        def on_button(event):
            MainPygame(None if self.m_mercury.GetValue() == '' else eval(self.m_mercury.GetValue()),
                 None if self.v_mercury.GetValue() == '' else eval(self.v_mercury.GetValue()),
                 None if self.r_mercury.GetValue() == '' else eval(self.r_mercury.GetValue()),
                 None if self.t_mercury.GetValue() == '' else eval(self.t_mercury.GetValue()),
                 None if self.m_venus.GetValue() == '' else eval(self.m_venus.GetValue()),
                 None if self.v_venus.GetValue() == '' else eval(self.v_venus.GetValue()),
                 None if self.r_venus.GetValue() == '' else eval(self.r_venus.GetValue()),
                 None if self.t_venus.GetValue() == '' else eval(self.t_venus.GetValue()),
                 None if self.m_earth.GetValue() == '' else eval(self.m_earth.GetValue()),
                 None if self.v_earth.GetValue() == '' else eval(self.v_earth.GetValue()),
                 None if self.r_earth.GetValue() == '' else eval(self.r_earth.GetValue()),
                 None if self.t_earth.GetValue() == '' else eval(self.t_earth.GetValue()),
                 None if self.m_mars.GetValue() == '' else eval(self.m_mars.GetValue()),
                 None if self.v_mars.GetValue() == '' else eval(self.v_mars.GetValue()),
                 None if self.r_mars.GetValue() == '' else eval(self.r_mars.GetValue()),
                 None if self.t_mars.GetValue() == '' else eval(self.t_mars.GetValue()),
                 None if self.m_jupiter.GetValue() == '' else eval(self.m_jupiter.GetValue()),
                 None if self.v_jupiter.GetValue() == '' else eval(self.v_jupiter.GetValue()),
                 None if self.r_jupiter.GetValue() == '' else eval(self.r_jupiter.GetValue()),
                 None if self.t_jupiter.GetValue() == '' else eval(self.t_jupiter.GetValue()),
                 None if self.m_saturn.GetValue() == '' else eval(self.m_saturn.GetValue()),
                 None if self.v_saturn.GetValue() == '' else eval(self.v_saturn.GetValue()),
                 None if self.r_saturn.GetValue() == '' else eval(self.r_saturn.GetValue()),
                 None if self.t_saturn.GetValue() == '' else eval(self.t_saturn.GetValue()),
                 None if self.m_uranus.GetValue() == '' else eval(self.m_uranus.GetValue()),
                 None if self.v_uranus.GetValue() == '' else eval(self.v_uranus.GetValue()),
                 None if self.r_uranus.GetValue() == '' else eval(self.r_uranus.GetValue()),
                 None if self.t_uranus.GetValue() == '' else eval(self.t_uranus.GetValue()),
                 None if self.m_neptune.GetValue() == '' else eval(self.m_neptune.GetValue()),
                 None if self.v_neptune.GetValue() == '' else eval(self.v_neptune.GetValue()),
                 None if self.r_neptune.GetValue() == '' else eval(self.r_neptune.GetValue()),
                 None if self.t_neptune.GetValue() == '' else eval(self.t_neptune.GetValue()),
                 None if self.m_moon.GetValue() == '' else eval(self.m_moon.GetValue()),
                 None if self.v_moon.GetValue() == '' else eval(self.v_moon.GetValue()),
                 None if self.r_moon.GetValue() == '' else eval(self.r_moon.GetValue()),
                 None if self.t_moon.GetValue() == '' else eval(self.t_moon.GetValue()),
                 None if self.m_sun.GetValue() == '' else eval(self.m_sun.GetValue()),
                 None if self.v_sun.GetValue() == '' else eval(self.v_sun.GetValue()),
                 None if self.r_sun.GetValue() == '' else eval(self.r_sun.GetValue()),
                 None if self.t_sun.GetValue() == '' else eval(self.t_sun.GetValue()), self,
                 None if self.m_asteroid.GetValue() == '' else eval(self.m_asteroid.GetValue()),
                 None if self.v_asteroid.GetValue() == '' else eval(self.v_asteroid.GetValue()),
                 None if self.r_asteroid.GetValue() == '' else eval(self.r_asteroid.GetValue()),
                 None if self.t_asteroid.GetValue() == '' else eval(self.t_asteroid.GetValue())
                 )

        bmp = wx.Bitmap('button.png')
        self.st = wx.Button(self, pos=(1250, 330), size=(160, 70))
        self.st.SetBitmap(bmp)
        self.st.Bind(wx.EVT_BUTTON, on_button)



class MainFrame(wx.Frame):

    def __init__(self):
        wx.Frame.__init__(self, None, title='Main Frame', size=(800, 600))
        self.Maximize(True)
        self.SetBackgroundColour(wx.BLACK)
        panel = MyPanel(self)
        self.Show()
        wx_png = wx.Image('wx_background.png', wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        wx.StaticBitmap(panel, -1, wx_png)
        self.Show()


if __name__ == '__main__':
    app = wx.App(False)
    frame = MainFrame()
    app.MainLoop()
