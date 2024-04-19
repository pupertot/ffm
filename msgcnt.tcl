#!/hci/cis19.1/integrator/bin/hcitcl
global env
set hciroot $env(HCIROOT)
set ignore_sites {}
set ignore_threads {}
set ignore_processes {}
set site_list {}
set site ""
set EMAILFROM "cloverleaf_test@wellforce.org"
set EMAILTO "cesar.ruiz@wellforce.org,anthony.schmelzer@wellforce.org"

array set options {}
set options(-site) ""
set options(-debug) 0
set options(-help) 0
set options(-allsites) 0
set options(-reset) 0

while { [llength $argv] } {
    switch -glob -- [lindex $argv 0] {
        -s* { set argv [lassign $argv - options(-site)] }
        -h* { set options(-help) 1 ; set argv [lrange $argv 1 end] }
        -d* { set options(-debug) 1 ; set argv [lrange $argv 1 end] }
        -a* { set options(-allsites) 1 ; set argv [lrange $argv 1 end] }
        -r* { set options(-reset) 1 ; set argv [lrange $argv 1 end] }
        -- { set argv [lrange $argv 1 end] ; break }
        -* { error "unknown option: [lindex $argv 0]" }
        default break
    }
}
if { $options(-help) == 1 } {
    puts "\nSyntax:"
    puts {  msgcnt -s <site> [-allsites] [-reset] [-help] [-debug]}
    puts "      -s <site>           - The site to run the message count report for."
    puts "      -allsites           - Use this option to run the report for every site."
    puts "      -reset              - Use this option to reset message counts."
    puts "      -help               - Displays this help text."
    puts "      -debug              - Allows various things to be written to the screen during execution."
    return ""
}

set debug $options(-debug)

if { $options(-site) != "" } {
    set site $options(-site)
}

if { $debug == 1 } {
    puts "DEBUG:1:Options: [array get options]"
    puts "DEBUG:1:Other args: $argv"
}

if { $site == "" && $options(-allsites) == 0 } {
	puts "\n-allsites was not provided as an argument and you did not specify a site using -site.\n"
    return ""
} 

if { $site != "" } {
    lappend site_list $site
}

if { $options(-allsites) == 1 } {
    set site_list [split [exec grep environs $hciroot/server/server.ini] \;]
}

set site_name ""
set live_thread_info {}
set ncfg_thread_info {}
set thread_list {}
set process_list {}
set site_totals {}
set out_cnt 0
set in_cnt 0
set total_in 0
set total_out 0
set total_cnt 0
set site_in_total 0
set site_out_total 0
set body ""
set thread ""
set ts [clock format [clock seconds] -format {%m-%d-%Y @ %I:%M:%S %p}]
set fnts [clock format [clock seconds] -format {%Y%m%d%H%M%S}]
set subject ""
set logpath ""
set logdir "/hci/cloverleaf/data/stats"
set fn ""
set fs ""
set line ""
set do_email 0

catch {
    file mkdir $logdir 
    set fn "message_count_${fnts}_[expr round(rand() * 1000000000)]"
    set logpath "${logdir}/${fn}.csv"
    set fs [open $logpath a+]
}

if { [file exists $logpath] == -1 } {
    return -code error "Could not create/open file:  ${logdir}/${fn}.csv"    
} else {
    if { $debug == 1 } {
        puts "File successfully created:  $logpath"
    }
}

set subject "Message counts for $ts \n"
set body "Message counts for $ts \n"
set body "${body}\nFor more details, see report here:\n${logpath}\n\n"

foreach site $site_list {    
    set site_in_total 0
    set site_out_total 0
	set site_name [file tail $site]
    set thread_list {}
	if { [lsearch -exact $ignore_sites $site_name] == -1 } {
        set do_email 1
		ChangeSite $site_name
        puts "\nSite: $site_name"
		netcfgLoad ${hciroot}/${site_name}/NetConfig
		catch { msiAttach }
		set process_list [netcfgGetProcList]
		foreach process $process_list {			
			catch { set thread_list [netcfgGetProcConns $process] }
			foreach thread $thread_list {
				catch {					
					set live_thread_info [lrange [exec hcicmd -p hcimonitord -t d -c "statusrpt $thread"] 2 end]
					keylget live_thread_info $thread live_thread_info
					
                    if { $live_thread_info == "" } { 
                        puts "Couldn't retrieve thread info for $thread"
                        continue
                    }
					
                    keylget live_thread_info MSGSIN in_cnt
                    keylget live_thread_info MSGSOUT out_cnt

                    # Output file in /hci/cloverleaf/data/stats/
                    set line "${site},${process},${thread},${in_cnt},${out_cnt}"
                    puts $fs $line

                    # Screen / process log
                    puts "Site - Thread:    $site_name - $thread"
                    puts "In: $in_cnt"
                    puts "Out: $out_cnt"
                    puts ""
                    
                    set total_in [expr $total_in + $in_cnt]
                    set total_out [expr $total_out + $out_cnt]
                    set total_cnt [expr $total_cnt + $total_in + $total_out]
                    set site_in_total [expr $site_in_total + $in_cnt]
                    set site_out_total [expr $site_out_total + $out_cnt]
                }
            }
        }
        set body "${body}\nSite : ${site_name}"
        set body "${body}\n  Total inbound for site ${site_name}: $site_in_total"
        set body "${body}\n  Total outbound for site ${site_name}: $site_out_total"
        set body "${body}\n  Combined in/out total for site ${site_name}: [expr $site_in_total + $site_out_total]\n"
        
        puts "Total inbound for site ${site_name}: $site_in_total"
        puts "Total outbound for site ${site_name}: $site_out_total"
        puts "Combined in/out total for site ${site_name}: [expr $site_in_total + $site_out_total]"
        puts "\n"
        catch { msiDetach }

        if { $options(-reset) == 1 } {
            set err_txt ""
            catch { [exec hcimsiutil -X] } err_txt
            puts "hcimsiutil -X catch results:  $err_txt"
        }
    }
}

close $fs

set body "${body}\n\n\n  Total inbound across all sites: $total_in"
set body "${body}\n  Total outbound across all sites: $total_out"
set body "${body}\n  Combined in/out total for all sites: [expr $total_in + $total_out]"

puts "Total inbound across all sites: $total_in"
puts "Total outbound across all sites: $total_out"
puts "Combined in/out total for all sites: [expr $total_in + $total_out]"

send_email -s $subject -b $body -f $EMAILFROM -r $EMAILTO

return ""