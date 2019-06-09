#! /bin/bash
# created by qinyangyang @ 2019-06-01

ip=$(awk '/^ip/{print $3}' ./conf/server.conf)
port=$(awk '/^port/{print $3}' ./conf/server.conf)

run_file=echo_server.py
pid_file=./conf/server.pid
log_file=./log/server_run.log

function check(){
    echo "check ..."
    pid=`cat $pid_file 2>/dev/null`
    run_count=`ps -p $pid 2>/dev/null | wc -l`
    if [ "$run_count" -ge "2" ]
    then
        echo "Process $pid is running."
    else
        echo "Process $pid is NOT running !!"
        return 1
    fi
    return 0
}

function start(){
    echo "start..."
    nohup python $run_file $ip $port > $log_file 2>&1 & echo $! > $pid_file
    t=0
    while [ $t -lt 5 ]
    do
        if check
        then
            break
        fi
        sleep 1s
        t=$(($t + 1))
    done
    echo "done"
}

function stop(){
    echo "stop ..."
    pid=`cat $pid_file 2>/dev/null`
    kill -9 $pid
    sleep 1s
    echo "done"
}

function restart(){
    if check
    then
        stop
    fi
    start
}

check_is_started(){
    if check
    then
        exit 0
    else
        exit 1
    fi
}

check_is_stoped(){
    if check
    then
        exit 1
    else
        exit 0
    fi
}

if [ "$1" = "start" ]
    then
    if check
        then
        echo "Process already running, EXIT"
    else
        start
    fi
    check_is_started
elif [ "$1" = "stop" ]
    then
    stop
    check_is_stoped
elif [ "$1" = "restart" ]
    then
    restart
    check_is_started
elif [ "$1" = "status" ]
    then
    check_is_started
else
    echo "Usage:"
    echo "    $0 [start|stop|restart|status]"
fi
