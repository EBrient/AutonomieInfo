from kivy.uix.widget import Widget
from kivy.app import App
from kivy.core.window import Window
from kivy.clock import Clock
from random import randint
from kivy.graphics import Rectangle
from kivy.graphics import Ellipse
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.graphics.context_instructions import Color
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.behaviors import ButtonBehavior



class Character(Widget):
    def __init__(self, canvas):
       self.canvas = canvas
       self.center_y = 100
       self.center_x = 200
       self.width = 50
       self.height = 20
       self.stop = False
       self.up = 0
       self.canvas.add(Color(1, 0.4, 0.4))
       with self.canvas:
           self.dessin = Ellipse(size=self.size, pos=self.pos)

    def move(self, keycode):
       if keycode == (273, 'up'):
           if self.center_y < 550:
               # self.up = 1
               self.center_y += 3
       if keycode == (274, 'down'):
           if self.center_y > 50:
               self.center_y -= 3
       if keycode == (275, 'right'):
           if self.center_x < 800:
               self.center_x += 3
       if keycode == (276, 'left'):
           if self.center_x > 50 :
               self.center_x -= 3
       self.dessin.pos = self.pos

    def collision(self, obs):
       if self.collide_widget(obs):
           self.stop = True


# def airmove(self):
#     if self.center_y > 100:
#         self.center_y += self.up*4
#     if self.center_y == 300:
#         self.up = -1
#     self.dessin.pos = self.pos


class Obstacle(Widget):
    def __init__(self, canvas):
       self.canvas = canvas
       self.height = randint(50, 100)
       self.width = self.height
       self.speed = randint(1, 4)
       self.center_x = 800
       self.center_y = randint(50, 500)
       self.canvas.add(Color(0.5, 0.5, 0.6))
       with self.canvas:
           self.dessin = Rectangle(size=(self.height, self.width), pos=self.pos)


    def move_well(self):
       self.center_x -= self.speed
       if self.center_x < -200:
           self.center_x = 900
           self.center_y = randint(50, 500)
       self.dessin.pos = self.pos
    def move_away(self):
       self.center_x -= self.speed
       self.dessin.pos = self.pos


class MultipleObstacles(Widget):
 def __init__(self, canvas):
    self.canvas = canvas
    self.Obs = []

 def ajouter(self, canvas):
    self.Obs.append(Obstacle(canvas))

class Score(Widget):
 def __init__(self, canvas):
     self.lescore = 0
     self.count = 0
     self.canvas = canvas
     self.center_y = 600
     self.center_x = 400
     with self.canvas:
         self.dessin = Label(size=(50, 50), pos=self.pos, text=str(self.lescore), font_size=30)

 def scoreup(self):
     self.count += 1
     if self.count == 10:
         self.lescore += 1
         self.count = 0
     self.dessin.text = str(self.lescore)

class ArcadeGame(Widget):

  def __init__(self, **kwargs):
      super(ArcadeGame, self).__init__(**kwargs)
      self._keyboard = Window.request_keyboard(self, 'text')
      self._keyboard.bind(on_key_down=self._on_keyboard_down)
      self._keyboard.bind(on_key_up=self._on_keyboard_up)
      self.key1 = (0, '')
      self.key2 = (0, '')
      img=Image(source="nebula_brown.PNG", size=(800, 600))
      self.add_widget(img)
      self.obs = MultipleObstacles(self.canvas)
      self.character = Character(self.canvas)
      self.score = Score(self.canvas)
      self.test = True
      self.meilleurs_scores = []
      self.ok = True

  def poke_bouton(self, instance):
      self.perdu = Label(text=('Votre vaisseau est détruit'))
      self.perdu.pos = (300, 400)
      self.perdu.size = (200, 100)
      self.perdu.font_size = Window.size[0]*0.05
      a = self.meilleurs_scores[0]
      for i in range(len(self.meilleurs_scores)):
          a = max(a, self.meilleurs_scores[i])
      self.print_ms = Label(text = str(a))
      self.print_ms.pos = (400, 500)
      self.print_ms.font_size = Window.size[0]*0.04
      self.BS = Label(text='Best Score : ')
      self.BS.pos = (300, 500)
      self.BS.font_size = Window.size[0]*0.04
      self.bouton = Button(text=('Reessayer'))
      self.bouton.pos = (200, 100)
      self.bouton.size = (400, 300)
      self.bouton.font_size = Window.size[0]*0.1
      self.bouton.bind(on_press=self.redemarre)
      self.add_widget(self.bouton)
      self.add_widget(self.perdu)
      self.add_widget(self.print_ms)
      self.add_widget(self.BS)

  def redemarre(self, instance):
      self.bouton.pos = (900, 900)
      self.character.stop = False
      self.canvas.clear()
      img=Image(source="nebula_brown.PNG", size=(800, 600))
      self.add_widget(img)
      self.obs = MultipleObstacles(self.canvas)
      self.character = Character(self.canvas)
      self.score = Score(self.canvas)
      Clock.schedule_interval(self.update, 1.0 / 200.0)
      self.ok = True




  def _on_keyboard_down(self, keyboard, keycode, text, message):
      if keycode == (275, 'right') or keycode == (276, 'left'):
          self.key1 = keycode

      if keycode == (273, 'up') or keycode == (274, 'down'):
          self.key2 = keycode

  def _on_keyboard_up(self, keyboard, keycode):
      if keycode == self.key1:
          self.key1 = (0, '')
      if keycode == self.key2:
          self.key2 = (0, '')


  def update(self, dt):
       self.score.scoreup()
      # self.character.airmove()
       self.character.move(self.key1)
       self.character.move(self.key2)
       for i in range(len(self.obs.Obs)):
           self.character.collision(self.obs.Obs[i])
       if len(self.obs.Obs) >= 13:
           for i in range(len(self.obs.Obs) - 13):
               self.obs.Obs[i].move_away()
           for j in range(len(self.obs.Obs)-13, len(self.obs.Obs)):
               self.obs.Obs[j].move_well()
       else:
           for i in range(len(self.obs.Obs)):
               self.obs.Obs[i].move_well()
       if self.character.stop:
           self.ok = False
           Clock.schedule_once(self.poke_bouton)
           Clock.unschedule(self.update)
           self.meilleurs_scores.append(self.score.lescore)




  def create_block(self, dt):
      if self.ok:
        self.obs.ajouter(self.canvas)

class ArcadeApp(App):
  def build(self):
      game = ArcadeGame()
      Clock.schedule_interval(game.update, 1.0 / 200.0)
      game.create_block(1)
      Clock.schedule_interval(game.create_block, 4)
      return game


if __name__ == '__main__':
  ArcadeApp().run()




