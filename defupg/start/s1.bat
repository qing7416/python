sqlcmd -I -S 10.205.1.1,1433    -U sa    -P 123asd!@#    -d db1     -i .\bos_oilpump\stat_bos_oilpumpsum.sql
sqlcmd -I -S 10.205.1.1,1433    -U sa    -P 123asd!@#    -d db2     -i .\bos_oilpump\stat_bos_oilpumpsum.sql
exit
