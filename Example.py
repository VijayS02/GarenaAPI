import matplotlib.pyplot as plt
from scipy.ndimage.filters import gaussian_filter1d

from Information import rolling_average
from User import User

if __name__ == "__main__":
    WINDOW_SIZE = 30

    # Example of user creation
    user = User("GregaryBack")
    user.get_games(3000, True)

    # Print out all possible games
    user.show_latest_games(None)

    # Get user KDA data
    kds, kdas, kills, time = user.get_kds(None)
    kds, kdas, kills = rolling_average(kds, WINDOW_SIZE), \
                       rolling_average(kdas, WINDOW_SIZE), rolling_average(kills, WINDOW_SIZE)

    # Plot the KDA data.
    plt.plot(time[:len(kds)], kds, label="KDS")
    plt.plot(time[:len(kdas)], kdas, label="KDAS")
    plt.plot(time[:len(kills)], kills, label="Kills")
    plt.legend()
    plt.show()
    # user.game_data[0].get_game_information()
