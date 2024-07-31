import matplotlib.pyplot as plt 

class ShowEverything:

    def __init__(self, ticker, int_ticker_trade):
        self.tick_name = [tick[0] for tick in ticker[int_ticker_trade]]

    def PlotEvery(self, df):
        fig = plt.figure(figsize=(30,20))
        ax1 = fig.add_subplot(331)
        ax2 = fig.add_subplot(332)
        ax3 = fig.add_subplot(333)
        ax4 = fig.add_subplot(334)
        ax5 = fig.add_subplot(335)
        ax6 = fig.add_subplot(336)
        ax7 = fig.add_subplot(337)
        ax8 = fig.add_subplot(338)
        ax9 = fig.add_subplot(339)

        ax1.plot(df[f"{self.tick_name[0]}-close"], label=f"{self.tick_name[0]}_Price", alpha=0.5)
        ax1.scatter(df.index, df[f"{self.tick_name[0]}-Buy"], color="g", marker="^",lw=4)
        ax1.scatter(df.index, df[f"{self.tick_name[0]}-Sell"], color="r", marker="v",lw=4)
        ax1.legend(loc="upper right")

        ax2.plot(df[f"{self.tick_name[1]}-close"], label=f"{self.tick_name[1]}_Price", alpha=0.5)
        ax2.scatter(df.index, df[f"{self.tick_name[1]}-Buy"], color="g", marker="^",lw=4)
        ax2.scatter(df.index, df[f"{self.tick_name[1]}-Sell"], color="r", marker="v",lw=4)
        ax2.legend(loc="upper right")

        ax3.plot(df[f"{self.tick_name[2]}-close"], label=f"{self.tick_name[2]}_Price", alpha=0.5)
        ax3.scatter(df.index, df[f"{self.tick_name[2]}-Buy"], color="g", marker="^",lw=4)
        ax3.scatter(df.index, df[f"{self.tick_name[2]}-Sell"], color="r", marker="v",lw=4)
        ax3.legend(loc="upper right")

        ax4.plot(df[f"{self.tick_name[3]}-close"], label=f"{self.tick_name[3]}_Price", alpha=0.5)
        ax4.scatter(df.index, df[f"{self.tick_name[3]}-Buy"], color="g", marker="^",lw=4)
        ax4.scatter(df.index, df[f"{self.tick_name[3]}-Sell"], color="r", marker="v",lw=4)
        ax4.legend(loc="upper right")

        ax5.plot(df[f"{self.tick_name[4]}-close"], label=f"{self.tick_name[4]}_Price", alpha=0.5)
        ax5.scatter(df.index, df[f"{self.tick_name[4]}-Buy"], color="g", marker="^",lw=4)
        ax5.scatter(df.index, df[f"{self.tick_name[4]}-Sell"], color="r", marker="v",lw=4)
        ax5.legend(loc="upper right")

        ax6.plot(df[f"{self.tick_name[5]}-close"], label=f"{self.tick_name[5]}_Price", alpha=0.5)
        ax6.scatter(df.index, df[f"{self.tick_name[5]}-Buy"], color="g", marker="^",lw=4)
        ax6.scatter(df.index, df[f"{self.tick_name[5]}-Sell"], color="r", marker="v",lw=4)
        ax6.legend(loc="upper right")

        ax7.plot(df[f"{self.tick_name[6]}-close"], label=f"{self.tick_name[6]}_Price", alpha=0.5)
        ax7.scatter(df.index, df[f"{self.tick_name[6]}-Buy"], color="g", marker="^",lw=4)
        ax7.scatter(df.index, df[f"{self.tick_name[6]}-Sell"], color="r", marker="v",lw=4)
        ax7.legend(loc="upper right")

        ax8.plot(df[f"{self.tick_name[7]}-close"], label=f"{self.tick_name[7]}_Price", alpha=0.5)
        ax8.scatter(df.index, df[f"{self.tick_name[7]}-Buy"], color="g", marker="^",lw=4)
        ax8.scatter(df.index, df[f"{self.tick_name[7]}-Sell"], color="r", marker="v",lw=4)
        ax8.legend(loc="upper right")

        ax9.plot(df[f"{self.tick_name[8]}-close"], label=f"{self.tick_name[8]}_Price", alpha=0.5)
        ax9.scatter(df.index, df[f"{self.tick_name[8]}-Buy"], color="g", marker="^",lw=4)
        ax9.scatter(df.index, df[f"{self.tick_name[8]}-Sell"], color="r", marker="v",lw=4)
        ax9.legend(loc="upper right")

        plt.show()
