SELECT 
name,
os,
region,
complex,
subsystem,
circuit,
segment,
domain,
role
FROM server_list
where upper(os) in ('LINUX','WINDOWS')
and region in($region)
and complex in($complex)
and subsystem in($subsystem)
and circuit in($circuit)
and segment in($segment)
and domain in($domain)
and role in($role)