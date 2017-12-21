echo "alert list"
netsil alert list
echo "create and delete Alert_Test_XYZ" 
netsil alert create "Alert_Test_XYZ" "avg(memPhysPctUsable) by (instance.host_name)" -o "<" -c .1 -w .2 -d 5
a=`netsil alert list | grep Alert_Test_XYZ | awk '{print $1}'`
netsil alert delete `echo $a`

echo "cpuSystem query"
netsil query run "A=avg(cpuSystem) by (instance.host_name)"

echo "dashboard list"
netsil dashboard list

echo "create and delete dashboard TEST_XYZ"
netsil dashboard create "TEST_XYZ"
a=`netsil dashboard list | grep -i test_xyz | awk '{print $1}'`
netsil dashboard delete `echo $a`

