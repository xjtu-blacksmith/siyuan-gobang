#include <iostream>
#include <cstdlib>
#include <cstring>
#include <conio.h>
using namespace std;
bool isin(int,int);
void showmessage();

// 光标类
class cursor  
{
private:            // 坐标
	int x;
	int y;
public:
	cursor(){x=7;y=7;}         // 从棋盘中心开始
    // getter
	int getX(){return x;}      
	int getY(){return y;}
    // 越界判断
	bool left(){if(x>0)x-=1;else return false;return true;}
	bool right(){if(x<14)x+=1;else return false;return true;}
	bool up(){if(y>0)y-=1;else return false;return true;}
	bool down(){if(y<14)y+=1;else return false;return true;}
    // setter
	bool moveto(int tx,int ty){if(isin(tx,ty)){x=tx;y=ty;return true;}else return false;}
};

// 棋盘类
class chessboard
{
private:
	int flag[15][15];      // 棋盘数组
	cursor handle;         // 棋盘对应的控制光标

	void f2c(int fg)       // 代号转化为输出字符
	{
		switch(fg)
		{
			case 0:cout<<"╋";break;  // 空棋盘
			case 2:cout<<"○";break;  // 白棋
			case 3:cout<<"●";break;  // 黑棋
		}
	}

	void show(int player)  // 画棋盘，对做GUI参考价值不大
	{
		int x=handle.getX();
		int y=handle.getY();
		cout<<"======================================"<<endl
			<<"===西安交通大学“思源”杯五子棋竞赛==="<<endl
			<<"======================================"<<endl<<endl
			<<"    ＡＢＣＤＥＦＧＨＩＪＫＬＭＮＯ"<<endl<<"  ┏";
		for(int i=0;i<15;i++)
			cout<<"┯";
		cout<<"┓"<<endl;
		for(int i=0;i<15;i++)
		{
			if(i<9)
				cout<<" ";
			cout<<i+1<<"┠";
			for(int j=0;j<15;j++){
				if(i==x&&j==y)
					cout<<"⊕";
				else
					f2c(flag[i][j]);
			}
			cout<<"┨"<<endl;
			
		}
		cout<<"  ┗";
		for(int i=0;i<15;i++)
			cout<<"┷";
		cout<<"┛"<<endl;
		cout<<"======================================"<<endl;
		if(player==2)
			cout<<"黑方[执棋○]                  [●]白方"<<endl;
		else
			cout<<"黑方[○]                  [执棋●]白方"<<endl;
	}

	bool setchessman(int player)   // 放棋子
	{
		int x=handle.getX();
		int y=handle.getY();
		if(flag[x][y]!=0)         // 已有棋子
			return false;
		else
			flag[x][y]=player;    // 放置当前玩家对应的棋子
		return true;
	}

	bool checkrange(int player)   // 检查是否有玩家获胜
	{
		int x=handle.getX();
		int y=handle.getY();
		cursor detector;
		for(int i=-2;i<=2;i++){
			if(detector.moveto(x+i,y)&&isin(x+i-2,y)&&isin(x+i+2,y)&&checkline(detector,player,1))
				return true;
			if(detector.moveto(x,y+i)&&isin(x,y+i-2)&&isin(x,y+i+2)&&checkline(detector,player,2))
				return true;
			if(detector.moveto(x+i,y+i)&&isin(x+i-2,y+i-2)&&isin(x+i+2,y+i+2)&&checkline(detector,player,3))
				return true;
			if(detector.moveto(x+i,y-i)&&isin(x+i-2,y-i-2)&&isin(x+i+2,y-i+2)&&checkline(detector,player,4))
				return true;
		}
		return false;
	}

    // 检查每一条线的情况
	bool checkline(cursor& detector,int player,int para)
	{
		int x=detector.getX();
		int y=detector.getY();
		int p=1;      // 做乘法的基底
		int q;
		if(player==2)
			q=32;     // 32=2*2*2*2*2
		else
			q=243;    // 243=3*3*3*3*3
		switch(para)  // 确认哪一个方向
		{
			case 1:
				for(int i=-2;i<=2;i++)
					p*=flag[x+i][y];
					if(p==q)return true;
				break;
			case 2:
				for(int i=-2;i<=2;i++){
					p*=flag[x][y+i];
					if(p==q)return true;
				}
				break;
			case 3:
				for(int i=-2;i<=2;i++){
					p*=flag[x+i][y+i];
					if(p==q)return true;
				}
				break;
			case 4:
				for(int i=-2;i<=2;i++){
					p*=flag[x+i][y-i];
					if(p==q)return true;
				}
				break;

		}
		return false;
	}

	int findrange()        // 查禁手
	{
		int three=0;
		int four=0;
		int x=handle.getX();
		int y=handle.getY();
		for(int para=1;para<=4;para++)
		{
			if(find_three(para))
				three++;
			if(three>=2)   // 双三禁手（含三四、三三四等）
				return 3;
			if(find_four(para))
				four++;
			if(four>=2)    // 双四禁手
				return 4;
			if(find_long(para))  // 长连禁手
				return 1;
		}
		return 0;         // 未犯禁手
	}

	bool find_three(int para)  // 查三三禁手
	{
		int x=handle.getX();
		int y=handle.getY();
		switch(para){
		case 1:
			for(int i=-3;i<=0;i++)
			{
				if(isin(x+i-1,y)&&isin(x+i+3,y))
					if(flag[x+i][y]*flag[x+i+1][y]*flag[x+i+2][y]==8&&flag[x+i-1][y]+flag[x+i+3][y]==0)
						return true;
				else if(isin(x+i,y)&&isin(x+i+3,y))
					if(flag[x+i][y]*flag[x+i+1][y]*flag[x+i+3][y]==8&&flag[x+i+2][y]==0)
						return true;
					else if(flag[x+i][y]*flag[x+i+2][y]*flag[x+i+3][y]==8&&flag[x+i+1][y]==0)
						return true;

			}
			return false;
		case 2:
			for(int i=-3;i<=0;i++)
			{
				if(isin(x,y+i)&&isin(x,y+i+2))
					if(flag[x][y+i]*flag[x][y+i+1]*flag[x][y+i+2]==8&&flag[x][y+i-1]+flag[x][y+i+3]==0)
						return true;
				else if(isin(x,y+i)&&isin(x,y+i+3))
					if(flag[x][y+i]*flag[x][y+i+1]*flag[x][y+i+3]==8&&flag[x][y+i+2]==0)
						return true;
					else if(flag[x][y+i]*flag[x][y+i+2]*flag[x][y+i+3]==8&&flag[x][y+i+1]==0)
						return true;

			}
			return false;
		case 3:
			for(int i=-3;i<=0;i++)
			{
				if(isin(x+i,y+i)&&isin(x+i+2,y+i+2))
					if(flag[x+i][y+i]*flag[x+i+1][y+i+1]*flag[x+i+2][y+i+2]==8&&flag[x+i-1][y+i-1]+flag[x+i+3][y+i+3]==0)
						return true;
				else if(isin(x+i,y+i)&&isin(x+i+3,y+i+3))
					if(flag[x+i][y+i]*flag[x+i+1][y+i+1]*flag[x+i+3][y+i+3]==8&&flag[x+i+2][y+i+2]==0)
						return true;
					else if(flag[x+i][y+i]*flag[x+i+2][y+i+2]*flag[x+i+3][y+i+3]==8&&flag[x+i+1][y+i+1]==0)
						return true;
			}
			return false;
		case 4:
			for(int i=-3;i<=0;i++)
			{
				if(isin(x+i,y-i)&&isin(x+i+2,y-i-2))
					if(flag[x+i][y-i]*flag[x+i+1][y-i-1]*flag[x+i+2][y-i-2]==8&&flag[x+i-1][y-i+1]+flag[x+i+3][y-i-3]==0)
						return true;
				else if(isin(x+i,y-i)&&isin(x+i+3,y-i-3))
					if(flag[x+i][y-i]*flag[x+i+1][y-i-1]*flag[x+i+3][y-i-3]==8&&flag[x+i+2][y-i-2]==0)
						return true;
					else if(flag[x+i][y-i]*flag[x+i+2][y-i-2]*flag[x+i+3][y-i-3]==8&&flag[x+i+1][y-i-1]==0)
						return true;
			}
			return false;
		}
	}

	bool find_four(int para)   // 查四四禁手
	{
		int x=handle.getX();
		int y=handle.getY();
		switch(para)
		{
		case 1:
			for(int i=-4;i<=0;i++)
			{
				if(isin(x+i,y)&&isin(x+i+4,y)&&(isin(x+i-1,y)||isin(x+i+4,y)))
					if(flag[x+i][y]*flag[x+i+1][y]*flag[x+i+2][y]*flag[x+i+3][y]==16&&(flag[x+i-1][y]==0||flag[x+i+4][y]==0))
						return true;
				else if(isin(x+i,y)&&isin(x+i+4,y))
					if(flag[x+i][y]*flag[x+i+2][y]*flag[x+i+3][y]*flag[x+i+4][y]==16&&flag[x+i+1][y]==0)
						return true;
					else if(flag[x+i][y]*flag[x+i+1][y]*flag[x+i+3][y]*flag[x+i+4][y]==16&&flag[x+i+2][y]==0)
						return true;
					else if(flag[x+i][y]*flag[x+i+1][y]*flag[x+i+2][y]*flag[x+i+4][y]==16&&flag[x+i+3][y]==0)
						return true;
					else if(flag[x+i][y]*flag[x+i+1][y]*flag[x+i+2][y]*flag[x+i+3][y]==16&&flag[x+i+4][y]==0)
						return true;
			}
			return false;
		
		case 2:
			for(int i=-4;i<=0;i++)
			{
				if(isin(x,y+i)&&isin(x,y+i+4)&&(isin(x,y+i-1)||isin(x,y+i+4)))
					if(flag[x][y+i]*flag[x][y+i+1]*flag[x][y+i+2]*flag[x][y+i+3]==16&&(flag[x][y+i-1]==0||flag[x][y+i+4]==0))
						return true;
				else if(isin(x,y+i)&&isin(x,y+i+4))
					if(flag[x][y+i]*flag[x][y+i+2]*flag[x][y+i+3]*flag[x][y+i+4]==16&&flag[x][y+i+1]==0)
						return true;
					else if(flag[x][y+i]*flag[x][y+i+1]*flag[x][y+i+3]*flag[x][y+i+4]==16&&flag[x][y+i+2]==0)
						return true;
					else if(flag[x][y+i]*flag[x][y+i+1]*flag[x][y+i+2]*flag[x][y+i+4]==16&&flag[x][y+i+3]==0)
						return true;
					else if(flag[x][y+i]*flag[x][y+i+1]*flag[x][y+i+2]*flag[x][y+i+3]==16&&flag[x][y+i+4]==0)
						return true;
			}
			return false;

		case 3:
			for(int i=-4;i<=0;i++)
			{
				if(isin(x+i,y+i)&&isin(x+i+4,y+i+4)&&(isin(x+i-1,y+i-1)||isin(x+i+4,y+i+4)))
					if(flag[x+i][y+i]*flag[x+i+1][y+i+1]*flag[x+i+2][y+i+2]*flag[x+i+3][y+i+3]==16&&(flag[x+i-1][y+i-1]==0||flag[x+i+4][y+i+4]==0))
						return true;
				else if(isin(x+i,y+i)&&isin(x+i+4,y+i+4))
					if(flag[x+i][y+i]*flag[x+i+2][y+i+2]*flag[x+i+3][y+i+3]*flag[x+i+4][y+i+4]==16&&flag[x+i+1][y+i+1]==0)
						return true;
					else if(flag[x+i][y+i]*flag[x+i+1][y+i+1]*flag[x+i+3][y+i+3]*flag[x+i+4][y+i+4]==16&&flag[x+i+2][y+i+2]==0)
						return true;
					else if(flag[x+i][y+i]*flag[x+i+1][y+i+1]*flag[x+i+2][y+i+2]*flag[x+i+4][y+i+4]==16&&flag[x+i+3][y+i+3]==0)
						return true;
					else if(flag[x+i][y+i]*flag[x+i+1][y+i+1]*flag[x+i+2][y+i+2]*flag[x+i+3][y+i+3]==16&&flag[x+i+4][y+i+4]==0)
						return true;
			}
			return false;

		case 4:
			for(int i=-4;i<=0;i++)
			{
				if(isin(x+i,y-i)&&isin(x+i+4,y-i-4)&&(isin(x+i-1,y-i+1)||isin(x+i+4,y-i-4)))
					if(flag[x+i][y-i]*flag[x+i+1][y-i-1]*flag[x+i+2][y-i-2]*flag[x+i+3][y-i-3]==16&&(flag[x+i-1][y-i+1]==0||flag[x+i+4][y-i-4]==0))
						return true;
				else if(isin(x+i,y-i)&&isin(x+i+4,y-i-4))
					if(flag[x+i][y-i]*flag[x+i+2][y-i-2]*flag[x+i+3][y-i-3]*flag[x+i+4][y-i-4]==16&&flag[x+i+1][y-i-1]==0)
						return true;
					else if(flag[x+i][y-i]*flag[x+i+1][y-i-1]*flag[x+i+3][y-i-3]*flag[x+i+4][y-i-4]==16&&flag[x+i+2][y-i-2]==0)
						return true;
					else if(flag[x+i][y-i]*flag[x+i+1][y-i-1]*flag[x+i+2][y-i-2]*flag[x+i+4][y-i-4]==16&&flag[x+i+3][y-i-3]==0)
						return true;
					else if(flag[x+i][y-i]*flag[x+i+1][y-i-1]*flag[x+i+2][y-i-2]*flag[x+i+3][y-i-3]==16&&flag[x+i+4][y-i-4]==0)
						return true;
			}
			return false;
		}
	}

	bool find_long(int para)   // 查长连禁手
	{
		int x=handle.getX();
		int y=handle.getY();
		switch(para)
		{
		case 1:
			for(int i=-4;i<=-1;i++)
				if(isin(x+i,y)&&isin(x+i+5,y)){
					int p=1;
					for(int j=0;j<6;j++)
						p*=flag[x+i+j][y];
					if(p==64)
						return true;
				}
			return false;
		case 2:
			for(int i=-4;i<=-1;i++)
				if(isin(x,y+i)&&isin(x,y+i+5)){
					int p=1;
					for(int j=0;j<6;j++)
						p*=flag[x][y+i+j];
					if(p==64)
						return true;
				}
			return false;
		case 3:
			for(int i=-4;i<=-1;i++)
				if(isin(x+i,y+i)&&isin(x+i+5,y+i+5)){
					int p=1;
					for(int j=0;j<6;j++)
						p*=flag[x+i+j][y+i+j];
					if(p==64)
						return true;
				}
			return false;
		case 4:
			for(int i=-4;i<=-1;i++)
				if(isin(x+i,y-i)&&isin(x+i+5,y-i-5)){
					int p=1;
					for(int j=0;j<6;j++)
						p*=flag[x+i+j][y-i-j];
					if(p==64)
						return true;
				}
			return false;
		}
	}

public:
	char state[10];    // 记录游戏进行状态

	chessboard()
	{
		for(int i=0;i<15;i++)
		for(int j=0;j<15;j++)
			flag[i][j]=0;         // 清空棋盘
		strcpy(state,"gaming");   // 游戏进行中
	}

	int play(int player)
	{
		system("cls");
		show(player);
		char behave;
		behave=getch();           // 获取键盘输入字符
		switch(behave)
		{
			case 72:              // 左方向键
				handle.left();
				break;
			case 75:              // 上方向键
				handle.up();
				break;
			case 77:              // 下方向键
				handle.down();
				break;
			case 80:              // 右方向键
				handle.right();
				break;
			case 13:              // Enter键
				if(setchessman(player)){      // 尝试放棋子
					if(player==2)
					{
						switch(findrange())   // 黑方查禁手
						{
						case 0:
							break;
						case 1:
							cout<<"黑方长连禁手！"<<endl;
							strcpy(state,"close");
							break;
						case 3:
							cout<<"黑方三三禁手！"<<endl;
							strcpy(state,"close");
							break;
						case 4:
							cout<<"黑方四四禁手！"<<endl;
							strcpy(state,"close");
							break;
						}
					}
					if(checkrange(player)){    // 判断输赢
						if(player==2)
							cout<<"黑方胜！"<<endl;
						else if(player==3)
							cout<<"白方胜！"<<endl;
						strcpy(state,"win");
					}
					player=5-player;   // 对手接盘
				}
				break;
		}
		return player;
	}

};


int main()
{
	system("title “思源”杯五子棋竞赛");    // 更改窗口标题
	showmessage();                        // 显示开局信息
	chessboard game;
	int counter=2;                        // 黑方先行
	while(strcmp(game.state,"gaming")==0)
		counter=game.play(counter);
	system("pause");
}

bool isin(int x,int y)          // 判断越界
{
	if(x>=0&&x<15&&y>=0&&y<15)
		return true;
	return false;
}

void showmessage()
{
	cout<<"┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓"<<endl
		<<"┃  西安交通大学“思源”杯五子棋竞赛  ┃"<<endl
		<<"┃           竞赛规则宣读           ┃"<<endl
		<<"┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫"<<endl
		<<"┃1. 不得穿拖鞋入场。               ┃"<<endl
		<<"┃2. 入场前请出示学生证。           ┃"<<endl
		<<"┃3. 黑方先手，白方后手。用方向键控 ┃"<<endl
		<<"┃   制光标移动，\"Enter\"键落子。    ┃"<<endl
		<<"┃4. 查黑方的三三、四四和长连禁手。 ┃"<<endl
		<<"┃5. 在不违反禁手的前提下，先连五子 ┃"<<endl
		<<"┃   者获胜，颁发五元加餐卷一张。   ┃"<<endl
		<<"┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛"<<endl;
	system("pause");
	system("cls");
}