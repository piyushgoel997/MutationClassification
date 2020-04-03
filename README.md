Things that can be done - 

roc curves
make the likely ones to be 0.8 and 0.2 or something (but how do I make the val, test data ain this case)
10-fold validation
increase/decrease hidden layers
instead of size 51 take some other size of the sequence

Got better results when using 1D convolution instead of 2D convolution, actually makes sense because the data is a 1D sequence and if we make it 2D most of the inputs would nevertheless be 0.

How does 1D conv work on this? Does it take the 20 as the number of channels.