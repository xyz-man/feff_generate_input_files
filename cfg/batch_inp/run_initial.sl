#! /bin/bash -l
#SBATCH --job-name="O_ideal-Yb_p003=1.99270_01"
#SBATCH --ntasks=4
#SBATCH --output="STDOUT.general.dat"

# check whether echo has the -e option
if test "" = "-e" ; then ECHO=echo ; else ECHO="echo -e" ; fi

#============================================================
# Main part for corect install environment variables ====>>

echo ""
echo "==========================="
echo
echo "Job started on      `hostname`     `date`"
echo
module avail
echo
module list
echo

module load wien2k/17.1/intel/15.0.0/mkl/mpich/3.1.2/fftw/3.3.4/wien2k

module list

echo ""
echo "==========================="

echo "SLURM_JOB_ID = " $SLURM_JOB_ID
echo
echo "SLURM_JOB_NODES = " $SLURM_JOB_NODES
echo
echo "SLURM_JOB_NODELIST = " $SLURM_JOB_NODELIST
echo
echo "SLURM_NTASKS = " $SLURM_NTASKS
echo
echo "SLURM_CPUS_ON_NODE = " $SLURM_CPUS_ON_NODE
echo
echo "scontrol show jobid -dd"
scontrol show jobid -dd $SLURM_JOB_ID
echo
echo "============================="
# env
echo "============================="
echo

echo "Job started on      `hostname`     `date`"
echo

echo $PATH
echo ""
echo "==========================="
# env


#============================================================

#============================================================
#Create new STDOUT file but add number if filename already exists in bash
name0="STDOUT-N=$SLURM_NNODES-n=$SLURM_NTASKS_PER_NODE-np=$SLURM_NTASKS"
name="$name0-OMP=$OMP_NUM_THREADS.dat"
#name=STDOUT
if [[ -e $name ]] ; then
i=0
while [[ -e $name-$i ]] ; do
 let i++
done
    name=$name--$i
    fi
        touch $name
#cat $1 >> $name 
echo '============================' >> $name
#echo '===========================' >> $name
#echo "OMP_NUM_THREADS=$OMP_NUM_THREADS" >> $name
#env >> $name
echo "==============================================" >> $name

#============================================================
#
#
#============================================================
# Set time in start point:
START=$(date +%s);
# Adjust this line: it must point to a directory containing the MPI FEFF modules
FeffPath=/opt/feff/feff90/unix/MPI
# Adjust this line to meet your system configuration: "
MPICommand="mpirun -n $SLURM_NTASKS" 
# In this example, we are using 12 parallel threads on 3 cluster nodes
# (n17, n18, and n20) with 4 (or more) cores each.
# Other common mpirun options are: --hostfile ; --nolocal ; etc.
# The calculation will be (a little less than) 12 times faster than a non-parallel
# calculation on the same computer.
# There should be no need to edit the following lines:
$MPICommand $FeffPath/rdinp >> $name 2>&1
$MPICommand $FeffPath/dmdw >> $name 2>&1
$MPICommand $FeffPath/atomic >> $name 2>&1
$MPICommand $FeffPath/pot >> $name 2>&1
$MPICommand $FeffPath/screen >> $name 2>&1
$MPICommand $FeffPath/opconsat >> $name 2>&1
$MPICommand $FeffPath/xsph >> $name 2>&1
$MPICommand $FeffPath/fms >> $name 2>&1
$MPICommand $FeffPath/mkgtr >> $name 2>&1
$MPICommand $FeffPath/path >> $name 2>&1
$MPICommand $FeffPath/genfmt >> $name 2>&1
$MPICommand $FeffPath/ff2x >> $name 2>&1
$MPICommand $FeffPath/sfconv >> $name 2>&1
$MPICommand $FeffPath/compton >> $name 2>&1
$MPICommand $FeffPath/eels >> $name 2>&1
$MPICommand $FeffPath/ldos >> $name 2>&1
# Set time when program was finished:
END=$(date +%s);
echo '============================================='
echo 'Calculation time:'
echo $((END-START)) | awk '{printf "%02d:%02d\n",int($1/60), int($1%60)}'
echo '============================================='
