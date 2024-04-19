#!/hci/cis19.1/integrator/bin/hcitcl
global env
set hciroot $env(HCIROOT)
set ignore_sites {}
set ignore_threads {}
set ignore_processes {}
set EMAILFROM ""
set EMAILTO ""
set EMAILCC {}
set QDEPTH ""
set LASTRCVTIME ""
set LASTSENDTIME ""
set commit 0
set stats {}

set site [lindex $argv 0]
if { $site == "" } {
	set site_list [split [exec grep environs $hciroot/server/server.ini] \;]
} else {
	lappend site_list $site
}

set site_name ""
set live_thread_info {}
set ncfg_thread_info {}
set thread_list {}
set autostart ""
set ip ""
set is_server ""
set port ""
set type ""
set obqd ""
set status ""
set err_txt ""
set last_write ""
set body ""
set thread ""
set cert_file ""
set val ""
set do_restart 0
set do_alert 0
set label ""
set action ""
set dif ""
set dif_text ""
set ts ""
set subject ""
set action_msg ""
set hour ""
set min ""
set sec ""

foreach site $site_list {
	set site_name [file tail $site]
	if { [file exists /hci/cloverleaf/config/threadmon/${site_name}.cfg] == 1 } {
		source /hci/cloverleaf/config/threadmon/${site_name}.cfg
	} else {
		source /hci/cloverleaf/config/threadmon/default.cfg
	}	
	if { [lsearch -exact $ignore_sites $site_name] == -1 } {
		ChangeSite $site_name
		netcfgLoad ${hciroot}/${site_name}/NetConfig
		catch { msiAttach }
		set process_list [netcfgGetProcList]
		# Loop through all processes
		foreach process $process_list {
			if { [file exists /hci/cloverleaf/config/threadmon/${process}.cfg] == 1 } {
				source /hci/cloverleaf/config/threadmon/${process}.cfg
			} else {
				source /hci/cloverleaf/config/threadmon/default.cfg
			}
			catch { set thread_list [netcfgGetProcConns $process] }
			foreach thread $thread_list {
				if { [file exists /hci/cloverleaf/config/threadmon/${thread}.cfg] == 1 } {
					source /hci/cloverleaf/config/threadmon/${thread}.cfg
				} else {
					source /hci/cloverleaf/config/threadmon/default.cfg
				}
				set do_restart 0
                set do_alert 0
				catch {
					set ncfg_thread_info [netcfgGetConnData $thread]
					set live_thread_info [lrange [exec hcicmd -p hcimonitord -t d -c "statusrpt $thread"] 2 end]
					keylget live_thread_info $thread live_thread_info
					if { $live_thread_info == "" } { 
                        puts "Couldn't retrieve thread info for $thread"
                        continue
                    }
					
					keylget ncfg_thread_info AUTOSTART autostart
					keylget ncfg_thread_info PROTOCOL.HOST ip
					keylget ncfg_thread_info PROTOCOL.ISSERVER is_server
					keylget ncfg_thread_info PROTOCOL.PORT port
					keylget ncfg_thread_info PROTOCOL.TYPE type
					keylget ncfg_thread_info PROTOCOL.CERT_FILE cert_file
					
					#keylget live_thread_info OBDATAQD obqd
					#keylget live_thread_info PSTATUS status
					#keylget live_thread_info PLASTERRTEXT err_txt
					#keylget live_thread_info PLASTWRITE last_write
					
					if { $autostart == 1 } {
						set autostart "On"
					} else {
						set autostart "Off"
					}
					
					if { $is_server == 1 } {
						set ip "<Incoming thread>"
					}
					
					set body "Thread: ${thread}"
                    set body "${body}\n  Site : ${site_name}"
					set body "${body}\n  AUTOSTART = $autostart"
					set body "${body}\n  HOST = $ip"					
					set body "${body}\n  Port = $port"
					set body "${body}\n  Cert = $cert_file"
					set body "${body}\n  Type = $type"
					
					foreach item $stats {
						set stat [lindex $item 0]
						if { [keylget stats [lindex $item 0]] == 1 } {
							keylget labels $stat label
							keylget live_thread_info $stat val
							
							if { [lsearch -exact {PLASTREAD PLASTWRITE PLASTERROR} $stat] != -1 } {
								if { $val == 0 } {
                                    set ts "Never"
                                } else {
                                    set ts [clock format $val -format {%m-%d-%Y @ %H:%M:%S}]
                                }
								set body "${body}\n  ${label} = ${ts}"
							} else {
								set body "${body}\n  ${label} = ${val}"
							}
							
							if { $is_server != 1 } {
								#puts "stat $stat - val $val"
								if { $stat == "OBDATAQD" && $val > $QDEPTH } {
									keylget actions QDEPTH action
									# write to logfile
									# do action
									puts "Doing $action for $thread because Outbound Queue Depth (${val}) > $QDEPTH"
                                    set subject "Outbound Queue Depth > $QDEPTH on $thread"
                                    send_email -b $body -s $subject -f $EMAILFROM -r $EMAILTO -d
								}
								
								if { $stat == "PLASTWRITE" } {
									if { $val == 0 } {
                                        puts "Doing $action for $thread because according to thread statistics, nothing as ever been sent."
                                        set subject "Thread $thread has never sent a message"
                                        set body "${body}\n\n [keylget message NEVER]"
                                        send_email -b $body -s $subject -f $EMAILFROM -r $EMAILTO -d
                                    } else {
                                        set dif [expr [clock seconds] - $val]
                                        set hr [expr $dif / 3600]
                                        set min [expr ($dif % 3600) / 60]
                                        set sec [expr ($dif % 3600) % 60]
                                        set dif_text [sec2txt $dif] 
                                        if { $dif > $LASTSENDTIME } {
                                            keylget actions LASTSENDTIME action
                                            # write to logfile
                                            # do action
                                            puts "Doing $action for $thread because amount of time since last send (${dif_text}) > [sec2txt $LASTSENDTIME]"
                                        }
                                    }
								}
							}
							
							if { $is_server == 1 } {
								if { $stat == "PLASTWRITE" } {
									set dif [expr [clock seconds] - $val]
									if { $dif > $LASTRCVTIME } {
										keylget actions LASTRCVTIME action
										# write to logfile
										# do action
										puts "Doing $action for $thread because Time since last receive (${dif}) > $LASTRCVTIME"
									}
								}
							}
							
							if { $stat == "PSTATUS" } {
								if { $val != "up" } {
									keylget actions THREAD_STATUS action
									#write to logfile
									#do action
									puts "Doing $action for $thread because PSTATUS (${val}) is not up"
								}
							}
						}
					}
					
					#if { $last_write != 0 } {
					#	set last_write [clock format $last_write -format {%m-%d-%Y @ %H:%M:%S}]
					#} else {
					#	set last_write "Never/Unknown"
					#}
					
					# Process inbound threads
					
					# Process outbound threads
					
					#puts $body
					
					#puts [exec hcimsiutil -dd $thread]
					#set info [exec hcimsiutil -dd $thread]					
					#if { $commit == 1 } { exec hcicmd -p $process -c "$thread pstart" }
					#	puts "Restarting $thread lol   (site: ${site_name})"
				} err
				if { $err != "" } { puts "Error while processing sites/processes/threads: $err" }
			}
		}
		catch { msiDetach }
	}
}