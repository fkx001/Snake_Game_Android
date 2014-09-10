from kivy.app import App
from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.uix.button import Button
from kivy.properties import ObjectProperty
from sets import Set
import random


class SnakeApp(App):

	def build(self):
		game = SnakeGame()
		game.build_game()
		Clock.schedule_interval(game.update, 1.0 / 10.0)
		return game


class SnakeGame(Widget):

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
	start_game = ObjectProperty(None)
	game_started = False
	game_lose = False
	empty_position = Set()
	lose_button = ObjectProperty(None)
	foods = {}

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
		self.start_game = Button(
			text = "Start Game"
		)
		self.start_game.bind(on_release = self.start_game_action)
		self.add_widget(self.start_game)
		self.game_started = False
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

	def start_game_action(self, button):
		self.remove_widget(self.start_game)
		self.game_started = True
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

	def game_over(self):
		self.lose_button = Button(
			text = "Game Over"
		)
		self.lose_button.pos = [self.top * 0.05, self.top * 0.05]
		self.lose_button.size = [self.top * 0.45, self.top * 0.45]
		self.lose_button.bind(on_release = self.reset_game_action)
		self.add_widget(self.lose_button)

	def reset_game_action(self, button):
		self.remove_widget(self.lose_button)
		self.build_game()

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
		self.start_game.pos = [self.top * 0.05, self.top * 0.05]
		self.start_game.size = [self.top * 0.45, self.top * 0.45]
		self.print_board()
		if self.game_started and not self.game_lose:
			self.time += 1
			if self.time >= self.move_time:
				self.move_once()
				if self.game_lose:
					self.game_over()
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
