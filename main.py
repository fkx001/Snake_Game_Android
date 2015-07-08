from kivy.app import App
from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.uix.button import Button
from kivy.properties import ObjectProperty
from sets import Set
import random


class SnakeApp(App):

	def build(self):
		self.icon = "./snake_icon.png"
		game = SnakeGame()
		game.build_game()
		Clock.schedule_interval(game.update, 1.0 / 10.0)
		return game

class SnakeGame(Widget):

	status = 0
	present_widget = ObjectProperty(None)
	last_difficulty = 0

	def build_game(self):
		self.status = 0
		self.present_widget = SnakeGameStart(
			size = self.size,
			pos = self.pos
		)
		self.present_widget.veryeasy.bind(on_release = self.start_game1)
		self.present_widget.easy.bind(on_release = self.start_game2)
		self.present_widget.medium.bind(on_release = self.start_game3)
		self.present_widget.hard.bind(on_release = self.start_game4)
		self.present_widget.veryhard.bind(on_release = self.start_game5)
		self.add_widget(self.present_widget)

	def start_game(self, difficulty):
		self.remove_widget(self.present_widget)
		self.present_widget = SnakeGamePlaying(
			size = self.size,
			pos = self.pos
		)
		self.present_widget.set_difficulty(difficulty)
		self.present_widget.build_game()
		self.add_widget(self.present_widget)
		self.status = 1
		self.last_difficulty = difficulty

	def start_game1(self, button):
		self.start_game(1)

	def start_game2(self, button):
		self.start_game(2)

	def start_game3(self, button):
		self.start_game(3)

	def start_game4(self, button):
		self.start_game(4)

	def start_game5(self, button):
		self.start_game(5)

	def try_agian(self, button):
		self.start_game(self.last_difficulty)

	def reset(self, button):
		self.remove_widget(self.present_widget)
		self.build_game()

	def gameover(self):
		self.status = 2
		self.remove_widget(self.present_widget)
		self.present_widget = SnakeGameOver(
			size = self.size,
			pos = self.pos
		)
		self.present_widget.tryagian.bind(on_release = self.try_agian)
		self.present_widget.goback.bind(on_release = self.reset)
		self.add_widget(self.present_widget)

	def update(self, dt):
		if self.status == 0:
			self.present_widget.set_size(self.top)
			self.present_widget.set_pos(self.top)
		elif self.status == 1:
			self.present_widget.update(dt)
			if self.present_widget.game_lose:
				self.gameover()
		elif self.status == 2:
			self.present_widget.set_size(self.top)
			self.present_widget.set_pos(self.top)


class SnakeGameStart(Widget):

	veryeasy = ObjectProperty(None)
	easy = ObjectProperty(None)
	medium = ObjectProperty(None)
	hard = ObjectProperty(None)
	veryhaed = ObjectProperty(None)

	def set_size(self, rootop):
		sizex = rootop
		sizey = rootop / 5
		self.veryeasy.size = [sizex, sizey]
		self.easy.size = [sizex, sizey]
		self.medium.size = [sizex, sizey]
		self.hard.size = [sizex, sizey]
		self.veryhard.size = [sizex, sizey]

	def set_pos(self, rootop):
		self.veryeasy.pos = [0, 0]
		self.easy.pos = [0, rootop / 5]
		self.medium.pos = [0, rootop / 5 * 2]
		self.hard.pos = [0, rootop / 5 * 3]
		self.veryhard.pos = [0, rootop / 5 * 4]


class SnakeGameOver(Widget):

	tryagian = ObjectProperty(None)
	goback = ObjectProperty(None)

	def set_size(self, rootop):
		sizex = rootop
		sizey = rootop / 2
		self.tryagian.size = [sizex, sizey]
		self.goback.size = [sizex, sizey]

	def set_pos(self, rootop):
		self.tryagian.pos = [0, 0]
		self.tryagian.pos = [0, rootop / 2]
	
class SnakeGamePlaying(Widget):

	move_time = 5
	nrows = 20
	ncols = nrows
	snakeposition = []
	time = 0
	squares = []
	# directions:
	# 1: right
	# 2: up
	# 3: left
	# 4: down
	direction = 1
	game_lose = False
	empty_position = Set()
	foods = {}

	def set_difficulty(self, difficulty):
		if difficulty == 1:
			self.move_time = 10
		elif difficulty == 2:
			self.move_time = 5
		elif difficulty == 3:
			self.move_time = 3
		elif difficulty == 4:
			self.move_time = 2
		elif difficulty == 5:
			self.move_time = 1

	def build_game(self):
		self.snakeposition = [
			[int(self.nrows / 2) - 1, int(self.ncols / 2) - 1],
			[int(self.nrows / 2) - 2, int(self.ncols / 2) - 1],
			[int(self.nrows / 2) - 3, int(self.ncols / 2) - 1],
			[int(self.nrows / 2) - 4, int(self.ncols / 2) - 1],
			[int(self.nrows / 2) - 5, int(self.ncols / 2) - 1]
		]
		self.time = 0
		for square in self.squares:
			self.remove_widget(square)
		self.squares = []
		self.direction = 1
		self.game_lose = False
		self.empty_position = Set()
		for i in range(0, self.nrows * self.ncols):
			self.empty_position.add(i)
		for coordinate in self.snakeposition:
			convertednum = coordinate[0] * self.ncols + coordinate[1]
			self.empty_position.remove(convertednum)
		for foodnum in self.foods:
			self.remove_widget(self.foods[foodnum])
		self.foods = {}
		self.add_food()

	def add_food(self):
		foodnum = random.sample(self.empty_position, 1)[0]
		foodi = foodnum / self.ncols
		foodj = foodnum % self.ncols
		side_length = self.top * 0.9 / self.nrows
		left = self.top * 0.05
		bottom = self.top * 0.05
		food = Food()
		food.set_pos(left + side_length * foodi, bottom + side_length * foodj)
		food.set_size(side_length)
		self.add_widget(food)
		self.foods[foodnum] = food		

	def print_board(self):
		for square in self.squares:
			self.remove_widget(square)
		self.squares = []
		side_length = self.top * 0.9 / self.nrows
		left = self.top * 0.05
		bottom = self.top * 0.05
		for k in range(0, len(self.snakeposition)):
			i = self.snakeposition[k][0]
			j = self.snakeposition[k][1]
			square = Square()
			square.set_pos(left + side_length * i, bottom + side_length * j)
			square.set_size(side_length)
			self.add_widget(square)
			self.squares.append(square)

	def move_once(self):
		tailposition = self.snakeposition[len(self.snakeposition) - 1]
		tailpositionnum = tailposition[0] * self.ncols + tailposition[1]
		self.empty_position.add(tailpositionnum)
		for i in range(len(self.snakeposition) - 1, 0, -1):
			self.snakeposition[i][0] = self.snakeposition[i - 1][0]
			self.snakeposition[i][1] = self.snakeposition[i - 1][1]
		if self.direction == 1:
			self.snakeposition[0][0] += 1
		elif self.direction == 2:
			self.snakeposition[0][1] += 1
		elif self.direction == 3:
			self.snakeposition[0][0] -= 1
		elif self.direction == 4:
			self.snakeposition[0][1] -= 1
		headposition = self.snakeposition[0]
		if headposition[0] < 0 or headposition[0] > self.ncols - 1 or headposition[1] < 0 or headposition[1] > self.nrows - 1:
			self.game_lose = True
			return
		headpositionnum = headposition[0] * self.ncols + headposition[1]
		if headpositionnum not in self.empty_position:
			self.game_lose = True
			return
		else:
			self.empty_position.remove(headpositionnum)
		if headpositionnum in self.foods:
			tailposition = [tailpositionnum / self.ncols, tailpositionnum % self.ncols]
			self.empty_position.remove(tailpositionnum)
			self.snakeposition.append(tailposition)
			self.remove_widget(self.foods[headpositionnum])
			del self.foods[headpositionnum]
			self.add_food()

	def update(self, dt):
		self.print_board()
		self.time += 1
		if self.time >= self.move_time:
			self.move_once()
			self.time = 0

	def on_touch_move(self, touch):
		if touch.dx > touch.dy and touch.dx > -touch.dy and (self.direction == 2 or self.direction == 4):
			self.direction = 1
		elif touch.dx < touch.dy and touch.dx < -touch.dy and (self.direction == 2 or self.direction == 4):
			self.direction = 3
		elif touch.dy > touch.dx and touch.dy > -touch.dx and (self.direction == 1 or self.direction == 3):
			self.direction = 2
		elif touch.dy < touch.dx and touch.dy < -touch.dx and (self.direction == 1 or self.direction == 3):
			self.direction = 4


class Square(Widget):

	def set_pos(self, x, y):
		self.pos = [x, y]

	def set_size(self, side_length):
		self.size = [side_length, side_length]


class Food(Widget):

	def set_pos(self, x, y):
		self.pos = [x, y]

	def set_size(self, side_length):
		self.size = [side_length, side_length]


if __name__ == "__main__":
	SnakeApp().run()
