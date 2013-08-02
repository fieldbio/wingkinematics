#!/usr/bin/env python
import csv
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import getopt
import sys
from pylab import *


def main(file):

	cycle=input("input the % of time in Downstroke: ")


# input files

	inFile = open(file,"r")
    	lines = inFile.readlines()		


    	Data= np.zeros(((len(lines)-1),48))



    	for N in range(1,len(lines)):

		temp = str(lines[N]).split(',')    		

		Data[N-1,:]=(float(temp[0]),float(temp[1]),float(temp[2]),float(temp[3]),float(temp[4]),float(temp[5]),float(temp[6]),float(temp[7]),float(temp[8]),float(temp[9]),float(temp[10]),float(temp[11]),float(temp[12]),float(temp[13]),float(temp[14]),float(temp[15]),float(temp[16]),float(temp[17]),float(temp[18]),float(temp[19]),float(temp[20]),float(temp[21]),float(temp[22]),float(temp[23]),float(temp[24]),float(temp[25]),float(temp[26]),float(temp[27]),float(temp[28]),float(temp[29]),float(temp[30]),float(temp[31]),float(temp[32]),float(temp[33]),float(temp[34]),float(temp[35]),float(temp[36]),float(temp[37]),float(temp[38]),float(temp[39]),float(temp[40]),float(temp[41]),float(temp[42]),float(temp[43]),float(temp[44]),float(temp[45]),float(temp[46]),float(temp[47]))

	Data=Data*25.4	#convert in to mm

##################################################################
# wing root estimation

#   	root= np.zeros(((len(lines)-1),12))

#	root[:,0]=(Data[:,0]*4+Data[:,3])/5
#	root[:,1]=(Data[:,1]*4+Data[:,4])/5
#	root[:,2]=((Data[:,2]*4+Data[:,5])/5)-10


#	root[:,3]=(Data[:,6]*4+Data[:,9])/5
#	root[:,4]=(Data[:,7]*4+Data[:,10])/5
#	root[:,5]=((Data[:,8]*4+Data[:,11])/5)-10

#	root[:,6]=(Data[:,18]*4+Data[:,21])/5
#	root[:,7]=(Data[:,19]*4+Data[:,22])/5
#	root[:,8]=((Data[:,20]*4+Data[:,23])/5)-10

#	root[:,9]=(Data[:,24]*4+Data[:,27])/5
#	root[:,10]=(Data[:,25]*4+Data[:,28])/5
#	root[:,11]=((Data[:,26]*4+Data[:,29])/5)-10


###############################################################
#wingbeat trace

	fig1=plt.figure()
	ax1 = Axes3D(fig1, azim=-225, elev=20)
	ax1.plot(Data[:,0],Data[:,1], Data[:,2], c='g') # R shoulder
	ax1.plot(Data[:,3],Data[:,4], Data[:,5], c='b') # R wing
	ax1.plot(Data[:,6],Data[:,7], Data[:,8], c='c') # L shoulder 
	ax1.plot(Data[:,9],Data[:,10], Data[:,11], c='r') # L wing
	ax1.plot(Data[:,12],Data[:,13], Data[:,14], c='k') # head
	ax1.plot(Data[:,15],Data[:,16], Data[:,17], c='m') # tail
	ax1.plot(Data[:,18],Data[:,19], Data[:,20], c='g') # R root down
	ax1.plot(Data[:,21],Data[:,22], Data[:,23], c='b') # L Root down


	ax1.plot(Data[:,24],Data[:,25], Data[:,26], c='c') # R shoulder up
	ax1.plot(Data[:,27],Data[:,28], Data[:,29], c='r') # R wing up
	ax1.plot(Data[:,30],Data[:,31], Data[:,32], c='k') # L shoulder up
	ax1.plot(Data[:,33],Data[:,34], Data[:,35], c='m') # L wing up
	ax1.plot(Data[:,36],Data[:,37], Data[:,38], c='c') # head up
	ax1.plot(Data[:,39],Data[:,40], Data[:,41], c='r') # tail up
	ax1.plot(Data[:,42],Data[:,43], Data[:,44], c='k') # R root up
	ax1.plot(Data[:,45],Data[:,46], Data[:,47], c='m') # L root up


	ax1.set_xlim3d(-60, 40)
	ax1.set_ylim3d(-50, 50)
	ax1.set_zlim3d(0, 100)
	ax1.set_aspect('equal', 'datalim')

#	plt.savefig('fig.svg')
#	plt.show()



######################################################################
#Descent rate

	Data_Mod= np.zeros(((len(lines)-1),48))
	Data_Mod[:,:]=Data[:,:]

#	root_Mod= np.zeros(((len(lines)-1),12))
#	root_Mod[:,:]=root[:,:]


	rate= (-2553) #mm/s
	descent= (np.linspace(99,0,100))*(rate)*(.00013)-(.00013*(-rate)*100)

#	Data_Mod[:,2]=Data_Mod[:,2]+descent2
	Data_Mod[:,5]=Data_Mod[:,5]+descent
	Data_Mod[:,20]=Data_Mod[:,20]+descent

#	Data_Mod[:,8]=Data_Mod[:,8]+descent
	Data_Mod[:,11]=Data_Mod[:,11]+descent
	Data_Mod[:,23]=Data_Mod[:,23]+descent

	
	Data2=np.vstack(((Data_Mod[:,18:21]),np.flipud((Data_Mod[:,3:6]))))
	Data2=np.insert(Data2,[200],Data2[0,:],axis=0)

	Data3=np.vstack(((Data_Mod[:,21:24]),np.flipud((Data_Mod[:,9:12]))))
	Data3=np.insert(Data3,[200],Data3[0,:],axis=0)


	descent2=(np.linspace(99,0,100))*(rate)*(.00013)

#	Data_Mod[:,20]=Data_Mod[:,20]+descent2
	Data_Mod[:,29]=Data_Mod[:,29]+descent2
	Data_Mod[:,44]=Data_Mod[:,44]+descent2

#	Data_Mod[:,26]=Data_Mod[:,26]+descent2
	Data_Mod[:,35]=Data_Mod[:,35]+descent2
	Data_Mod[:,47]=Data_Mod[:,47]+descent2
	
	Data4=np.vstack(((Data_Mod[:,42:45]),np.flipud((Data_Mod[:,27:30]))))
	Data4=np.insert(Data4,[200],Data4[0,:],axis=0)

	Data5=np.vstack(((Data_Mod[:,45:48]),np.flipud((Data_Mod[:,33:36]))))
	Data5=np.insert(Data5,[200],Data5[0,:],axis=0)




#########################################################################
#vortex rings


#	plt.clf()
	fig2=plt.figure()
	ax2 = Axes3D(fig2, azim=-225, elev=90)
	ax2.plot(Data2[:,0],Data2[:,1], Data2[:,2], c='r')
	ax2.plot(Data3[:,0],Data3[:,1], Data3[:,2], c='b')

#	ax.plot(Data2[0:100,0],Data2[0:100,1], Data2[0:100,2], c='g')
#	ax.plot(Data3[0:100,0],Data3[0:100,1], Data3[0:100,2], c='g')




	ax2.plot(Data4[:,0],Data4[:,1], Data4[:,2], c='r')
	ax2.plot(Data5[:,0],Data5[:,1], Data5[:,2], c='b')

#	ax.plot(Data4[0:100,0],Data4[0:100,1], Data4[0:100,2], c='g')
#	ax.plot(Data5[0:100,0],Data5[0:100,1], Data5[0:100,2], c='g')




	ax2.set_xlim3d(-60, 40)
	ax2.set_ylim3d(-50, 50)
	ax2.set_zlim3d(0, 100)
	ax2.set_aspect('equal', 'datalim')

#	ax2.plot(Data[:,12],Data[:,13], Data[:,14], c='k') # head
#	ax2.plot(Data[:,15],Data[:,16], Data[:,17], c='m') # tail
###########################################################################


	Output=np.vstack(((Data2[:,0:4]),(Data3[:,0:4]),(Data4[:,0:4]),(Data5[:,0:4]),(Data[:,12:15]),(Data[:,15:18])))

#	Output=np.vstack(((Data2[:,0:4]),(Data3[:,0:4]),(Data[:,12:15]),(Data[:,15:18])))

	Writer = csv.writer(open("vortex.csv", 'w'), delimiter=',', quotechar=',', quoting=csv.QUOTE_MINIMAL)
	for N in range(0,len(Output)):
		Writer.writerow(Output[N])



###########################################################################
#side view svg

#	plt.savefig('fig.svg')
	plt.show()

	plt.clf()
	plt.plot(Data2[:,0], Data2[:,2], c='b')
	plt.axis((-70,50,-50,100))
	axes().set_aspect('equal', 'datalim')
	plt.savefig('fig2.svg')

#######################################################################3
	# position and angle of wing relative to horizontal line through shoulder
	RShoulder=vstack((Data[:,0:3],Data[:,24:27]))
	RWing=vstack((Data[:,3:6],Data[:,27:30]))
	LShoulder=vstack((Data[:,6:9],Data[:,30:33]))
	LWing=vstack((Data[:,9:12],Data[:,33:36]))

	RShoulder=vstack((RShoulder,RShoulder))
	RWing=vstack((RWing,RWing))
	LShoulder=vstack((LShoulder,LShoulder))
	LWing=vstack((LWing,LWing))


		#Transform Shoulder and Wingtip to Shoulder centered Frame Of Reference
		
	RShoulder_Sh = RShoulder-RShoulder
	RWing_Sh = RWing - RShoulder

	LShoulder_Sh = LShoulder-LShoulder
	LWing_Sh = LWing - LShoulder

	NegXaxis=(-1,0,0)

		#Project Wingtip onto XY Plane

	RWing_ShXY = RWing - RShoulder
	RWing_ShXY[:,2]=0	

	LWing_ShXY = LWing - LShoulder
	LWing_ShXY[:,2]=0


	Length_RWing_Sh = sqrt((RWing_Sh[:,0]**2)+(RWing_Sh[:,1]**2)+(RWing_Sh[:,2]**2))
	Length_RWing_ShXY = sqrt((RWing_ShXY[:,0]**2)+(RWing_ShXY[:,1]**2)+(RWing_ShXY[:,2]**2))


	R_Elevation_Ground= transpose(degrees(arccos((RWing_Sh[:,0]*RWing_ShXY[:,0]+RWing_Sh[:,1]*RWing_ShXY[:,1])/((Length_RWing_Sh)*(Length_RWing_ShXY)))*np.sign([RWing_Sh[:,2]])))

	R_Position_Ground= degrees(arccos((RWing_ShXY[:,0]*NegXaxis[0]+RWing_ShXY[:,1]*NegXaxis[1]+RWing_ShXY[:,2]*NegXaxis[2])/(Length_RWing_ShXY)))

	
	Length_LWing_Sh = sqrt((LWing_Sh[:,0]**2)+(LWing_Sh[:,1]**2)+(LWing_Sh[:,2]**2))
	Length_LWing_ShXY = sqrt((LWing_ShXY[:,0]**2)+(LWing_ShXY[:,1]**2)+(LWing_ShXY[:,2]**2))


	L_Elevation_Ground= transpose(degrees(arccos((LWing_Sh[:,0]*LWing_ShXY[:,0]+LWing_Sh[:,1]*LWing_ShXY[:,1])/((Length_LWing_Sh)*(Length_LWing_ShXY)))*np.sign([LWing_Sh[:,2]])))

	L_Position_Ground= degrees(arccos((LWing_ShXY[:,0]*NegXaxis[0]+LWing_ShXY[:,1]*NegXaxis[1]+LWing_ShXY[:,2]*NegXaxis[2])/(Length_LWing_ShXY)))
		

	L_Elevation_Ground = nan_to_num(L_Elevation_Ground)
	R_Elevation_Ground = nan_to_num(R_Elevation_Ground)


#############################
	# position and angle of wing ROOT relative to horizontal line through shoulder
	RRoot=vstack((Data[:,18:21],Data[:,42:45]))
	LRoot=vstack((Data[:,21:24],Data[:,45:48]))

	RRoot=vstack((RRoot,RRoot))
	LRoot=vstack((LRoot,LRoot))

		#Transform Shoulder and Root to Shoulder centered Frame Of Reference
	
	
	RRoot_Sh = RRoot - RShoulder

	LRoot_Sh = LRoot - LShoulder

		#Project Root onto XY Plane

	RRoot_ShXY = RRoot - RShoulder
	RRoot_ShXY[:,2]=0	

	LRoot_ShXY = LRoot - LShoulder
	LRoot_ShXY[:,2]=0


	Length_RRoot_Sh = sqrt((RRoot_Sh[:,0]**2)+(RRoot_Sh[:,1]**2)+(RRoot_Sh[:,2]**2))
	Length_RRoot_ShXY = sqrt((RRoot_ShXY[:,0]**2)+(RRoot_ShXY[:,1]**2)+(RRoot_ShXY[:,2]**2))


	R_Root_Elevation_Ground= transpose(degrees(arccos((RRoot_Sh[:,0]*RRoot_ShXY[:,0]+RRoot_Sh[:,1]*RRoot_ShXY[:,1])/((Length_RRoot_Sh)*(Length_RRoot_ShXY)))*np.sign([RRoot_Sh[:,2]])))

	R_Root_Position_Ground= transpose(degrees(arccos((RRoot_ShXY[:,0]*NegXaxis[0]+RRoot_ShXY[:,1]*NegXaxis[1]+RRoot_ShXY[:,2]*NegXaxis[2])/(Length_RRoot_ShXY)))*-np.sign([RRoot_ShXY[:,1]]))
	

	
	Length_LRoot_Sh = sqrt((LRoot_Sh[:,0]**2)+(LRoot_Sh[:,1]**2)+(LRoot_Sh[:,2]**2))
	Length_LRoot_ShXY = sqrt((LRoot_ShXY[:,0]**2)+(LRoot_ShXY[:,1]**2)+(LRoot_ShXY[:,2]**2))


	L_Root_Elevation_Ground= transpose(degrees(arccos((LRoot_Sh[:,0]*LRoot_ShXY[:,0]+LRoot_Sh[:,1]*LRoot_ShXY[:,1])/((Length_LRoot_Sh)*(Length_LRoot_ShXY)))*np.sign([LRoot_Sh[:,2]])))

	L_Root_Position_Ground= transpose(degrees(arccos((LRoot_ShXY[:,0]*NegXaxis[0]+LRoot_ShXY[:,1]*NegXaxis[1]+LRoot_ShXY[:,2]*NegXaxis[2])/(Length_LRoot_ShXY)))*np.sign([LRoot_ShXY[:,1]]))
		

	L_Root_Elevation_Ground = nan_to_num(L_Root_Elevation_Ground)
	R_Root_Elevation_Ground = nan_to_num(R_Root_Elevation_Ground)


#############################

	p=float(2*cycle)
	q=float(200-p)
	
	#q=p
	#r=200-p
	
	print q/100

	a=arange(0,p,(p/100))
	b=arange(p,p+q,(q/100))
	c=arange(p+q,p+p+q,(p/100))
	d=arange(p+p+q,p+p+q+q,(q/100))

#	a=arange(0,100,1)
#	b=arange(100,150,.5)
#	c=arange(150,250,1)
#	d=arange(250,300,.5)
	
	
	Time=hstack((a,b,c,d))
	print shape(Time)


# plot all points 



	clf()	
#	figure(num=None, figsize=(7, 5), dpi=200)

	subplot(211)
	plot(Time[:],R_Position_Ground[:],c='b')
	plot(Time[:],L_Position_Ground[:],c='r')
	plot(Time[:],R_Root_Position_Ground[:],c='b')
	plot(Time[:],L_Root_Position_Ground[:],c='r')

	scatter((p,p+200),(0,0),marker='^')


	xlim((0,400))
	ylim((-20,180))	
	grid(True)




	subplot(212)
	plot(Time[:],R_Elevation_Ground[:],c='b')
	plot(Time[:],L_Elevation_Ground[:],c='r')
	plot(Time[:],R_Root_Elevation_Ground[:],c='b')
	plot(Time[:],L_Root_Elevation_Ground[:],c='r')


	scatter((p,p+200),(0,0),marker='^')

	scatter(77,0,c='r',marker='v')


	xlim((0,400))
	ylim((-80,20))
#	ylim((0,180))		
	grid(True)







#	show()	
	savefig('Dev.svg')
#	savefig('Pos.svg')








if __name__ == '__main__':

	try:
        	opts, args = getopt.getopt(sys.argv[1:], 'h', ['help'])
	

    	except getopt.error:
        	sys.stderr.write("%s: %s \nTry `%s --help` for more informatIon\n"
        		% (PROGNAME, e, PROGNAME))
        	sys.exit(1)


    	for o in opts:
        	if o in ('-h', '--help'):
        		usage(error=0)

    	if len(args) != 1:
        	usage()

    	main(args[0])

