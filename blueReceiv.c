#define MaxSizeOfMessage 35// 34 byte of data max (+ terminator)

const TMailboxIDs queue = mailbox1;//the mailbox where the PC will send the message

void readDataMsg()
{
	int mSizeOfMessage = cCmdMessageGetSize(queue);
	ubyte mBuffer[MaxSizeOfMessage];// no malloc with RobotC :(

	if (mSizeOfMessage <= 0)//there's no message
	{
		wait1Msec(1);//wait before we check again
		return;
	}
	if (mSizeOfMessage > MaxSizeOfMessage)// shouldn't happen but well, then we'll only read the first part of the message
	{
		mSizeOfMessage = MaxSizeOfMessage;
	}

	if (cCmdMessageRead(mBuffer, mSizeOfMessage, queue) == ioRsltSuccess)//we've successfully copied the message
	{
		mSizeOfMessage -= 1;// skip the terminator

		// do whatever you want here
		for (int i = 0; i < mSizeOfMessage; i++)
		{
			nxtDisplayBigTextLine(2," %d ", mBuffer[i]);
			wait(2);
		}
	}

	return;
}


task main ()
{
	eraseDisplay();
	while (true)
	{
		readDataMsg();
	}
}
