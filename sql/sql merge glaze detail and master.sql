select 
	master."Block ID", 
	master."GlazeColor", 
	detail."Block Line Number", 
	master."Project Number",
	detail."Current Location" 
	from "Mstr Block Template" as master	
	
	
left join "Mstr Block WS Detl" as detail		
	on master."Project Number" = detail."Project Number"
	and master."Block ID" = detail."Block ID"
	
	where master."Project Number" = 'P17-0881'
	and detail."Project Number" = 'P17-0881'
	and master."GlazeColor" = 'TAN w/ BLACK SP'

order by detail."Block Line Number"