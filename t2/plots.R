f <- function(s, r, b)
  return (1 - (1 - s**r)**b)

#y <- function(r)
#  return (0.6)


x <- seq(0,1,0.01)

plot(x, f(x, 8, 8), type="l", col="blue", axes = FALSE)
#lines(x, y(x), col="red")
ticks <- seq(0, 1, 0.1)       # sequence for ticks and labels

axis(1, at = ticks, labels = ticks)
axis(2, at = ticks, labels = ticks)

x = seq(1,15)
y = c(4,5,6,5,5,6,7,8,7,7,6,6,7,8,9)
plot(x,y,type="l",ylim=c(3,10))
lo <- loess(y~x)
xl <- seq(min(x),max(x), (max(x) - min(x))/1000)
out = predict(lo,xl)
lines(xl, out, col='red', lwd=2)

infl <- c(FALSE, diff(diff(out)>0)!=0)
points(xl[infl ], out[infl ], col="blue")

require(inflection)
require(RootsExtremaInflections)
d<-inflexi(x,y,1,length(x),5,5,plots=TRUE);d$an;d$finfl;