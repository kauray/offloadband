 
smg

player bandselection
    [band4g], [band5glow], [band5gmmwave], [band4gexec]  ,[band4gexectemp] , [band5glowexec] , [band5glowexectemp] , [band5gmmwaveexec], [band5gmmwaveexectemp]
endplayer

player environment
//    transmitter, battery, server, [devtranmission]
//    transmitter, [totransmit], [devtranmission], [serverexecution]
    [update4g], [update5glow], [update5gmmwave]
endplayer

const int pmax = 5;
const int latencym = 100;
const int tmax = 10;
const int slottime = 50;

const double e = 2.718281828459045;
const double ib = pcpu / 0.6;
const double b21 = -0.043;
const double b22 = -14.275;
const double vsoc = 0.96; // vsoc = cb / cfull * 1 V
const double b23 = 0.154;
//const double voc;
const double kd = 0.019;

const double b11 = -0.265;
const double b12 = -61.649;
const double b13 = -2.039;
const double b14 = 5.276;
const double b15 = -4.173;
const double b16 = 1.654;
const double b17 = 3.356;


// constants for p_device
const double ccf = 0.00642;
const double xcf = 1500;
const double xck = 0.01;
const double xcu = 0.05;
const double p0xcpu = 0.332;

const double p11;
const double p12;
const double p13;
const double p14;
const double p15;
const double p21;
const double p22;
const double p23;
const double p24;
const double p25;
const double p31;
const double p32;
const double p33;
const double p34;
const double p35;

global turn : [0..2] init 0;

//formula energyconsumed = floor(packetstransmitted + harvestedpackets);

//formula one = floor(level + cputil);

formula etdtlittle = batteryenergy - econsumedlittle;
formula etdtbig = batteryenergy - econsumedbig;

formula etdtserver4g = batteryenergy - econsumedserver4g;
formula etdtserver5glow = batteryenergy - econsumedserver5glow;
formula etdtserver5gmmwave = batteryenergy - econsumedserver5gmmwave;

formula econsumedlittle = slottime  * pcpulittle * e_loss;
formula econsumedbig = slottime  * pcpubig * e_loss;

formula econsumedserver4g = slottime  * pcpuserver4g * e_loss;
formula econsumedserver5glow = slottime  * pcpuserver5glow * e_loss;
formula econsumedserver5gmmwave = slottime  * pcpuserver5gmmwave * e_loss;


//full power
//formula p_device = pcpu + p3g + wifi; //p_device will be calculated in the module

//cpu power
formula p_device = pcpu; //p_device will be calculated in the module

formula pcpulittle = 1;
formula pcpubig = 5;

formula pcpuserver4g = 10;
formula pcpuserver5glow = 15;
formula pcpuserver5gmmwave = 20;

formula pcpu = ccf * xcf * (xck    + xcu) + p0xcpu;
//formula p3g = x3gon * ((c3gi * x3gi)  + (c3gf * x3gf)  + (c3gd * x3gd));
//formula wifi = xwon * ((cwflow * xwflow) + (cwfhigh * xwfhigh));


formula e_loss = slottime  * (ib * ib * b21* pow(e, ((b22*vsoc) + b23))) + (ib * voc * (pow(ib, kd) - 1));

formula voc = b11 * pow(e, (b12 * vsoc)) + 
        b13 * pow(vsoc, 4) + 
        b14 * pow(vsoc, 3) + 
        b15 * pow(vsoc, 2) + 
        b16 * vsoc + 
        b17  
        ; 

//model of temperature

const double tenv;
const double rcpuenv = 35.8;
const double rbatenv = 7.58;
const double rcpubat = 78.8; //to be calculated
const double pbatlittle = 6.67;
const double pbatbig = 33.33;
const double threshold = 40;

formula tempbatterylittle = tenv + (rcpuenv * rbatenv) / (rbatenv + rcpubat + rcpuenv) * pcpulittle ;
// + 
//((rcpuenv * rbatenv) + (rcpubat*rbatenv)) / (rbatenv + rcpubat + rcpuenv) * pbatlittle;

formula tempbatterybig = tenv + (rcpuenv * rbatenv) / (rbatenv + rcpubat + rcpuenv) * pcpubig  ;
//+ 
//((rcpuenv * rbatenv) + (rcpubat*rbatenv)) / (rbatenv + rcpubat + rcpuenv) * pbatbig;


//migration lock parameter
const int k = 3;

module selectband
    execution : [-1..2] init -1; // -1 initial, 0 band 4g, 1 bang 5glow, 2 5gmmwave
    
    //non-deterministic choice of on device computation versus offload to edge server
    [band4g] turn = 0 & execution = -1 -> (execution' = 0) & (turn' = 1);
    [band5glow] turn = 0 & execution = -1 -> (execution' = 1) & (turn' = 1);
    [band5gmmwave] turn = 0 & execution = -1 -> (execution' = 2) & (turn' = 1);

    //non-deterministic choice of migrate across server
    [band4gexec]  turn = 0 & execution = 0 & temp <= threshold -> (execution' = 0) & (turn' = 1);
    [band4gexec]  turn = 0 & execution = 0 & temp <= threshold -> (execution' = 1) & (turn' = 1);
    [band4gexec]  turn = 0 & execution = 0 & temp <= threshold -> (execution' = 2) & (turn' = 1);
    
    [band4gexectemp]  turn = 0 & execution = 0 & temp > threshold -> (execution' = 0) & (turn' = 1);
    
    [band5glowexec]  turn = 0 & execution = 1 & temp <= threshold -> (execution' = 0) & (turn' = 1);
    [band5glowexec]  turn = 0 & execution = 1 & temp <= threshold -> (execution' = 1) & (turn' = 1);
    [band5glowexec]  turn = 0 & execution = 1 & temp <= threshold -> (execution' = 2) & (turn' = 1);
    
    [band5glowexectemp]  turn = 0 & execution = 1 & temp > threshold -> (execution' = 0) & (turn' = 1);
    
    [band5gmmwaveexec]  turn = 0 & execution = 2 & temp <= threshold -> (execution' = 0) & (turn' = 1);
    [band5gmmwaveexec]  turn = 0 & execution = 2 & temp <= threshold -> (execution' = 1) & (turn' = 1);
    [band5gmmwaveexec]  turn = 0 & execution = 2 & temp <= threshold -> (execution' = 2) & (turn' = 1);
    
    [band5gmmwaveexectemp]  turn = 0 & execution = 2 & temp > threshold -> (execution' = 0) & (turn' = 1);
    [band5gmmwaveexectemp]  turn = 0 & execution = 2 & temp > threshold -> (execution' = 1) & (turn' = 1);
    
    [] turn = 0 & dtime = tmax -> true;
endmodule

module device
    batteryenergy : [0..28800] init 28800;
    //device battery

    temp : [10..90] init ceil(tenv);
    //battery temperature

    dtime : [0..tmax] init 0;
    
    //offloaded, determine the power consumption in terms of offload
    
    [update4g] turn = 1 & batteryenergy > 0 & dtime < tmax & execution = 0-> 
	(batteryenergy' = floor(etdtserver4g))  & (turn' = 0) & (dtime' = dtime + 1);
	
    [update5glow] turn = 1 & batteryenergy > 0 & dtime < tmax & execution = 1-> 
	(batteryenergy' = floor(etdtserver5glow)) & (turn' = 0) & (dtime' = dtime + 1);
	
    [update5gmmwave] turn = 1 & batteryenergy > 0 & dtime < tmax & execution = 2-> 
	(batteryenergy' = floor(etdtserver5gmmwave)) & (turn' = 0) & (dtime' = dtime + 1);

    //[updatebatteryoffload2] turn = 1 & execution = 1 & batteryenergy > 0 & dtime < tmax -> 
	//	(batteryenergy' = etdt) & (turn' = 3);
    [] dtime = tmax -> (dtime' = tmax);
endmodule

module server
    latency : [0..latencym] init 0;
    

    [update4g] turn = 1 & execution = 0 & dtime < tmax & batteryenergy > 0 ->
	 p31 : (latency' = 0)  + p32 : (latency' = 1) + p33 : (latency' = 2) + p34 : (latency' = 3) + p35 : (latency' = 4);

    [update5glow] turn = 1 & execution = 1 & dtime < tmax & batteryenergy > 0 ->
	 p31 : (latency' = 0)  + p32 : (latency' = 1) + p33 : (latency' = 2) + p34 : (latency' = 3) + p35 : (latency' = 4);

    [update5gmmwave] turn = 1 & execution = 2 & dtime < tmax & batteryenergy > 0 ->
	 p31 : (latency' = 0)  + p32 : (latency' = 1) + p33 : (latency' = 2) + p34 : (latency' = 3) + p35 : (latency' = 4);
endmodule

//module timer
//    [dtmax] dtime = tmax & turn = 4 -> (dtime' = dtime);
//    [devicerunning] dtime < tmax & turn = 4 -> (dtime' = dtime + 1);
//    [serverexecution] dtime < tmax & turn = 4 -> (dtime' = dtime + 1);
//endmodule

rewards "latency"
    latency = 0 : 500;
    latency = 1 : 400;
    latency = 2 : 300;
    latency = 3 : 200;
    latency = 4 : 100;
endrewards

rewards "nopref"
    true : 1;
endrewards

rewards "energy"
    true : batteryenergy;
endrewards

rewards "server"
    execution = 1 : 500;
endrewards

rewards "jointlatencyenergy"
    latency = 0 : 100;
    latency = 1 : 100;
    latency = 2 : 100;
    latency = 3 : 50;
    latency = 4 : 50;
    true : batteryenergy;
endrewards

rewards "eqlatency"
    latency = 0 : latency + batteryenergy;
    latency = 1 : latency + batteryenergy;
    latency = 2 : latency + batteryenergy;
    latency = 3 : latency + batteryenergy;
    latency = 4 : latency + batteryenergy;
//    tmig = 1 | tmig = 2 : -1;
//    mig = 1 | mig = 2 : -1;
//    latency = 0 & mig != 0 & tmig != 0: 0;
//    latency = 1 & mig != 0 & tmig != 0: 0;
//    latency = 2 & mig != 0 & tmig != 0: 0;
//    latency = 3 & mig != 0 & tmig != 0: 0;
//    latency = 4 & mig != 0 & tmig != 0: 0;
endrewards
