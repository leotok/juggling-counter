# Juggling Counter

Count how many times you throw your juggling balls in the air!

Stay in front of your webcam, run this program and start juggling. It will count how many times a ball passes one half of the screen height. If you stop for more than 1 second, your score resets.

## Requirements

- `python3`
- and a webcam.

Run the following to install the required libs

```shell
$ pip install -r requirements.txt
```

## How to use

```shell
$ python src/main.py
```

## Configuration

The default color for the balls to be recognized is `blue`.

If you want to use another color, you can run the helper script `src/range-detector.py` to verify which HSV range is ideal for you set.

```shell
$ python src/range-detector.py
```

Then, change the variables `color_lower` and `color_upper` with the desired values

Ex:
```python
# blue lower and upper bounds
color_lower = (82, 42, 14)
color_upper = (139, 244, 255)
```
