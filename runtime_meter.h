#ifndef RUNTIME_METER_H
#define RUNTIME_METER_H

#define RUNTIME_METER_SECONDS 1
#define RUNTIME_METER_MILLISECONDS 1000
#define RUNTIME_METER_MICROSECONDS 1000000
#define RUNTIME_METER_NANOSECONDS 1000000000
#define RUNTIME_METER_MINUTES (1/60.0)
#define RUNTIME_METER_HOURS (1/3600.0)
#define RUNTIME_METER_DAYS (1/86400.0)

#include <Windows.h>
#include <string>
#include <iostream>

using std::string;
using std::ostream;

class runtime_meter
{
	LARGE_INTEGER frequency, begin, end;

	bool inUse;
	long precision;
	bool longFormat;

	string ID;

	ostream* os;

	void streamInterval(const double& interval);
	string precisionToString(double);
public:
	runtime_meter(string ID, double precision, ostream* os = nullptr, bool longFormat = false);
	~runtime_meter();

	void start();
	double stop();

	void setPrecision(double prec);

};

#endif 