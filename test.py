import tictak

game = tictak.TikTakToe(1)
game.start("M")
while game.status():
    game.print_field()
    x, y = input().split(' ')
    game.move(int(x), int(y))
else:
    game.print_field()
