select 
DISTINCT
Name as name,
upper(OSFamily) as os,
Region as region,
Complex as complex,
Subsystem as subsystem,
Circuit as circuit,
Segment as segment,
Domain as domain,
Role as role
from dbo.viewAllServers
where upper(OSFamily) in ('LINUX','WINDOWS')
and Region in($region)
and Complex in($complex)
and Subsystem in($subsystem)
and Circuit in($circuit)
and Segment in($segment)
and Domain in($domain)
and Role in($role)