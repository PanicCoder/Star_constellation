from Super_Classes.Screen import create_screen
if(__name__ == "__main__"):
    create_screen()
    from Game_logic.Engine import Engine
    Engine().Loop() 