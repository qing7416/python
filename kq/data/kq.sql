--考勤数据表
create table kq(
	id int null,
	dept varchar(32),
	name varchar(31),
	kqdate datetime,
	kqtime varchar(10)
);

--找出每天最早和最晚的打卡时间作为上下班时间，18:30后下班记为加班（可调休，但无补助），20:00后下班记发补助
select 
	name,kqdate,
	case when min(kqtime) <> max(kqtime) then min(kqtime) when min(kqtime) = max(kqtime) and min(kqtime) < '12:00:00' then min(kqtime) else null end first_kqtime,
	case when min(kqtime) <> max(kqtime) then max(kqtime) when min(kqtime) = max(kqtime) and min(kqtime) >= '12:00:00' then min(kqtime) else null end last_kqtime,
	case when max(kqtime) >= '18:30' then max(kqtime) else null end Overtime1
	case when max(kqtime) >= '20:00' then max(kqtime) else null end Overtime2
from kq 
group by name,kqdate;