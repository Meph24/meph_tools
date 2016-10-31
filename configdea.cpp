
#ifndef DEACODER_STATEMASHINE
#define DEACODER_STATEMASHINE
struct deacoder_statemashine
{
	int q;
};
#endif

enum configdea_states
{
	trap = -1,		//default trap state
	q0 = 0,
	q1 = 1,
	q2 = 2,
	q3 = 3,
	q4 = 4,
	q5 = 5,
	q6 = 6,
	q7 = 7,
	q8 = 8,
	q9 = 9,

	NUM_CONFIGDEA_STATES
};

void configdea_init(deacoder_statemashine* M)
{
    M->q = configdea_states::q0;
}

void configdea_d(deacoder_statemashine* M, char sym)
{
    switch(M->q)
    {
    
		case configdea_states::q0:

			if(((sym == ' ')))
			{
			    M->q = configdea_states::q0;
			}

			else if(((sym == '#')))
			{
			    M->q = configdea_states::q1;
			}

			else
			{
			    M->q = configdea_states::trap;
			}

		break;

		case configdea_states::q1:

			if((((sym >= 'a') && (sym <= 'z')) || ((sym >= 'A') && (sym <= 'Z')) || (sym == '_')))
			{
			    M->q = configdea_states::q1;
			}

			else if(((sym == ' ')))
			{
			    M->q = configdea_states::q2;
			}

			else
			{
			    M->q = configdea_states::trap;
			}

		break;

		case configdea_states::q2:

			if(((sym == ' ')))
			{
			    M->q = configdea_states::q2;
			}

			else if((((sym >= 'a') && (sym <= 'z')) || ((sym >= 'A') && (sym <= 'Z')) || (sym == '_')))
			{
			    M->q = configdea_states::q3;
			}

			else
			{
			    M->q = configdea_states::trap;
			}

		break;

		case configdea_states::q3:

			if((((sym >= 'a') && (sym <= 'z')) || ((sym >= 'A') && (sym <= 'Z')) || (sym == '_')))
			{
			    M->q = configdea_states::q3;
			}

			else if(((sym == ' ')))
			{
			    M->q = configdea_states::q4;
			}

			else if(((sym == '=')))
			{
			    M->q = configdea_states::q5;
			}

			else
			{
			    M->q = configdea_states::trap;
			}

		break;

		case configdea_states::q4:

			if(((sym == '=')))
			{
			    M->q = configdea_states::q5;
			}

			else
			{
			    M->q = configdea_states::trap;
			}

		break;

		case configdea_states::q5:

			if(((sym == ' ')))
			{
			    M->q = configdea_states::q5;
			}

			else if((((1)&& (!(sym == ' '))&& (!(sym == '"')))))
			{
			    M->q = configdea_states::q6;
			}

			else if(((sym == '"')))
			{
			    M->q = configdea_states::q8;
			}

			else
			{
			    M->q = configdea_states::trap;
			}

		break;

		case configdea_states::q6:

			if((((1)&& (!(sym == ' ')))))
			{
			    M->q = configdea_states::q6;
			}

			else if(((sym == ' ')))
			{
			    M->q = configdea_states::q7;
			}

			else
			{
			    M->q = configdea_states::trap;
			}

		break;

		case configdea_states::q7:

			if(((sym == ' ')))
			{
			    M->q = configdea_states::q7;
			}

			else if((((sym >= 'a') && (sym <= 'z')) || ((sym >= 'A') && (sym <= 'Z')) || (sym == '_')))
			{
			    M->q = configdea_states::q3;
			}

			else if(((sym == '#')))
			{
			    M->q = configdea_states::q1;
			}

			else
			{
			    M->q = configdea_states::trap;
			}

		break;

		case configdea_states::q8:

			if((((1)&& (!(sym == '"'))&& (!(sym == '\\')))))
			{
			    M->q = configdea_states::q8;
			}

			else if(((sym == '\\')))
			{
			    M->q = configdea_states::q9;
			}

			else if(((sym == '"')))
			{
			    M->q = configdea_states::q7;
			}

			else
			{
			    M->q = configdea_states::trap;
			}

		break;

		case configdea_states::q9:

			if(((1)))
			{
			    M->q = configdea_states::q8;
			}

			else
			{
			    M->q = configdea_states::trap;
			}

		break;

		case configdea_states::trap:
		default:
		break;
		}
}

int configdea_exit(deacoder_statemashine* M)
{
	int cs = M->q;
	return ((M->q == q1) || (M->q == q2) || (M->q == q6) || (M->q == q7));
}

#include <iostream>
#include <string>

using std::endl;
using std::cout;
using std::string;

int main()
{
	deacoder_statemashine M;
	configdea_init(&M);
	cout << M.q << endl;

	string s = "#graphics fov =52 height= 42 name = \"deref\\ere\"";

	for (size_t i = 0; i < s.size(); i++)
	{
		configdea_d(&M, s[i]);
		if (!(i % 4)) cout << " ";
		cout << M.q;
	}

	cout << endl << configdea_exit(&M) << endl;

	getchar();
}