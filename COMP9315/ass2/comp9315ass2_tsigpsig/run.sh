rm *.o x1 x2 x3 create dump gendata insert select stats
rm R.*
make
echo
echo ---------------- Test 1 Running... ----------------
echo
./x1

echo
echo ---------------- Building Database... ----------------
echo
echo ---------------- Generating Data... ----------------
./gendata 5 4
echo ---------------- Creating Relationship... ----------------
./create R 5000 4 1000
echo ---------------- Checking Status... ----------------
./stats R
echo ---------------- Inserting Data... ----------------
./gendata 5000 4 | ./insert R
echo ---------------- Checking Status... ----------------
./stats R
echo ---------------- Showing All Data... ----------------
./dump R
echo ---------------- Executing Query... ----------------
./select  R  1000001,?,?  t
echo ---------------- Executing Query... ----------------
./select  R  ?,?,a3-002,a4-022  p
# echo ---------------- Executing Query... ----------------
# ./select  R  1000001,?,a3-002,?  t
# echo ---------------- Executing Query... ----------------
# ./select  R  1000001,?,a3-002,?  x

# echo
# echo ---------------- Test 2 Running... ----------------
# echo
# ./x2 1000001,?,?,?

# echo ---------------- Test 3 Running... ----------------
# echo
# ./x3