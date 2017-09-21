import time
from tqdm import tqdm


def main():
    for i in tqdm(range(1000)):
        time.sleep(.01)


if __name__ == '__main__':
    main()
