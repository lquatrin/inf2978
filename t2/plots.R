
f <- function(s, r, b)
  return (1 - (1 - s**r)**b)

#y <- function(r)
#  return (0.6)


x <- seq(0,1,0.01)

plot(x, f(x, 8, 16), type="l", col="blue", axes = FALSE)
#lines(x, y(x), col="red")
ticks <- seq(0, 1, 0.1)       # sequence for ticks and labels

axis(1, at = ticks, labels = ticks)
axis(2, at = ticks, labels = ticks)

