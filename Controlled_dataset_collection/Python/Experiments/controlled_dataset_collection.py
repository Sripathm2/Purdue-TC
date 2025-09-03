from configparser import ConfigParser
import os
import time
import random
from multiprocessing import Process
import subprocess
import datetime
import sys

def setup_config_and_space(cc_alg='cubic', link_delay='10', link_bw='1000'):
    print('INFO ** Setting up config **')
    os.system('cp ./Configurations/controlled_config.ini ./config.ini')

    print('changing link bandwidth and delay')
    os.system('sed -i \'12s/.*/link_delay = ' + link_delay + 'ms/\' ./config.ini')
    os.system('sed -i \'13s/.*/link_bw = ' + link_bw + '/\' ./config.ini')

    print('INFO ** setting up congestion control algorithm **')
    if 'bbr' in cc_alg:
        os.system('make setup-bbr-congestion-control-algorithm')
    else:
        os.system('make cc_alg=' + cc_alg + ' setup-congestion-control-algorithm')

    print('INFO ** Taking backup of config.ini **')
    os.system('cp ./config.ini ./config.ini.bak')

def disable_tso():
    results = os.popen("ifconfig -a | sed 's/[ \t].*//;/^\(lo\|\)$/d' | grep veth").readlines()
    for interface in results:
        os.system("sudo ethtool -K " + interface[:-2] + " tx off sg off tso off")


def start_topology():
    print('INFO ** changing config.ini for master_running = True topology **')
    config = ConfigParser()
    config.read('./config.ini')
    config['TOPOLOGY']['master_running'] = 'True'
    with open('./config.ini', 'w') as configfile:
        config.write(configfile)
    print('INFO ** Setting up topology **')
    os.system('make setup-topology')


def start_client_packet_capture(host_name, capture_as_text=True):
    print('INFO ** Starting host name capture **')
    if capture_as_text:
        os.system('make host_name=' + host_name + ' start-client-pcap-capture-as-text')
    else:
        os.system('make host_name=' + host_name + ' start-client-pcap-capture')


def start_switch_packet_capture(intf_name, capture_as_text=True):
    print('INFO ** Starting host name capture **')
    if capture_as_text:
        os.system('make intf_name=' + intf_name + ' start-switch-pcap-capture-as-text')
    else:
        intf_name_1 = intf_name.split(':')[0]
        capture_name_1 = intf_name.split(':')[1]
        os.system('make intf_name=' + intf_name_1 + ' capture_name=' + capture_name_1 + ' start-switch-pcap-capture')

def start_iperf_server():
    print('INFO ** Starting iperf server **')
    os.system('make start-iperf-server')

def start_iperf_client():
    print('INFO ** Starting iperf client **')
    os.system('make start-iperf-client')


def start_email_server():
    print('INFO ** Starting Email POP3 server **')
    os.system('make start-email-server')


def start_video_streaming_server():
    print('INFO ** Starting video Streaming server **')
    os.system('make start-video-streaming-server')

def start_video_conferncing_server():
    print('INFO ** Starting video conferencing server **')
    os.system('make start-video-conferencing-server')

def start_ftp_server():
    print('INFO ** Starting FTP server **')
    os.system('make start-ftp-server')


def start_web_server():
    print('INFO ** Starting web server **')
    os.system('make start-web-server')


def start_email_workload(email_client, number_of_emails):
    print('INFO ** Starting Email POP3 client **')
    os.system('make email_client=' + email_client + ' num_email=' + str(number_of_emails) + ' start-email-client ')


def start_video_streaming_workload(vs_client, video_index):
    print('INFO ** Starting video streaming client **')
    os.system('make vs_client=' + vs_client + ' video_index=' + str(video_index) + ' start-video-streaming-client')


def start_ftp_workload(ftp_client, num_files):
    print('INFO ** Starting ftp client **')
    os.system('make ftp_client=' + ftp_client + ' num_files=' + str(num_files) + ' start-ftp-client')


def start_web_workload(web_client, num_websites):
    print('INFO ** Starting ftp client **')
    os.system('make web_client=' + web_client + ' num_websites=' + str(num_websites) + ' start-web-client')


def start_Vc_reciever_workload(vc_client, call_length):
    print('INFO ** Starting video conferecing client **')
    os.system('make call_length=' + str(call_length+10) + ' vc_client=' + str(vc_client) + ' start-video-conferencing-receiver')


def run_all_experiments(workload, capture_on_switch=True, capture_as_text=False, capture_name='s1-eth5', start_iperf = False):
    p_topology = Process(target=start_topology, args=())
    p_topology.start()
    time.sleep(180)

    # os.system('make start-ftp-setup')

    disable_tso()

    p_iperf_server = Process(target=start_iperf_server, args=())
    p_iperf_server.start()
    p_email_server = Process(target=start_email_server, args=())
    p_email_server.start()
    p_video_streaming_server = Process(target=start_video_streaming_server, args=())
    p_video_streaming_server.start()
    p_ftp_server = Process(target=start_ftp_server, args=())
    p_ftp_server.start()
    p_web_server = Process(target=start_web_server, args=())
    p_web_server.start()
    p_video_conferencing_server = Process(target=start_video_conferncing_server, args=())
    p_video_conferencing_server.start()
    p_iperf_client = None
    if start_iperf:
        p_iperf_client = Process(target=start_iperf_client, args=())
        p_iperf_client.start()

    time.sleep(40)

    p_client1 = p_client2 = p_client3 = p_client4 = p_switch = None

    if not capture_on_switch:
        p_client1 = Process(target=start_client_packet_capture, args=('client1', capture_as_text))
        p_client1.start()

        p_client2 = Process(target=start_client_packet_capture, args=('client2', capture_as_text))
        p_client2.start()

        p_client3 = Process(target=start_client_packet_capture, args=('client3', capture_as_text))
        p_client3.start()

        p_client4 = Process(target=start_client_packet_capture, args=('client4', capture_as_text))
        p_client4.start()

    else:
        p_switch = Process(target=start_switch_packet_capture, args=('s1-eth5:'+capture_name, capture_as_text))
        p_switch.start()

    time.sleep(20)

    ### example workloads

    processes = []

    for work in workload:
        time.sleep(work[0])
        if work[1] == 'Web':
            p_work_load = Process(target=start_web_workload, args=(work[2], work[3]))
            p_work_load.start()
            processes.append(p_work_load)
        elif work[1] == 'Email':
            p_work_load = Process(target=start_email_workload, args=(work[2], work[3]))
            p_work_load.start()
            processes.append(p_work_load)
        elif work[1] == 'Vs':
            p_work_load = Process(target=start_video_streaming_workload, args=(work[2], work[3]))
            p_work_load.start()
            processes.append(p_work_load)
        elif work[1] == 'FTP':
            p_work_load = Process(target=start_ftp_workload, args=(work[2], work[3]))
            p_work_load.start()
            processes.append(p_work_load)
        elif work[1] == 'Vc':
            p_work_load_reciever = Process(target=start_Vc_reciever_workload, args=(work[2], work[3]))
            p_work_load_reciever.start()
            processes.append(p_work_load_reciever)


    for proc in processes:
        proc.join()

    time.sleep(20)

    try:
        if not capture_on_switch:
            p_client1.kill()
            p_client2.kill()
            p_client3.kill()
            p_client4.kill()
        else:
            p_switch.kill()
            

        if start_iperf:
            p_iperf_client.kill()

        p_iperf_server.kill()
        p_email_server.kill()
        p_video_streaming_server.kill()
        p_ftp_server.kill()
        p_web_server.kill()
        p_topology.kill()
    except:
        pass
    os.system('make clean')

def generate_workload(possible_applications, application_weights, possible_clients, clients_weights, number_of_tasks, min_app_limits, max_app_limits, min_wait_time, max_wait_time):
    workload = []
    vc_done = 0
    apps_list = random.choices(possible_applications, weights=application_weights, k=number_of_tasks*10)
    client_list = random.choices(possible_clients, weights=clients_weights, k=number_of_tasks*10)

    for index, app in enumerate(apps_list):
        time_to_sleep = random.uniform(min_wait_time, max_wait_time)
        parameter = -1
        if app == 'Web':
            parameter = random.randrange(min_app_limits[0], max_app_limits[0])
        elif app == 'Email':
            parameter = random.randrange(min_app_limits[1], max_app_limits[1])
        elif app == 'Vs':
            parameter = random.randrange(min_app_limits[2], max_app_limits[2])
        elif app == 'FTP':
            parameter = random.randrange(min_app_limits[3], max_app_limits[3])
        elif app == 'Vc' and vc_done == 0:
            parameter = random.randrange(min_app_limits[4], max_app_limits[4])
            vc_done += 1
        if parameter != -1:
            work = [time_to_sleep, app, client_list[index], parameter]
            workload.append(work)

    return workload[:number_of_tasks]

def main(possible_applications, application_weights, possible_clients, clients_weights, number_of_tasks, min_app_limits, max_app_limits, min_wait_time, max_wait_time, capture_on_switch=True, capture_as_text=False, run_throughput_graph=False, cc_alg='cubic'):
    #### main method
    setup_config_and_space(cc_alg=cc_alg)

    workload = generate_workload(possible_applications, application_weights, possible_clients, clients_weights, number_of_tasks, min_app_limits, max_app_limits, min_wait_time, max_wait_time)

    # one time running end
    run_all_experiments(workload, capture_on_switch, capture_as_text)

    if run_throughput_graph:
        os.system('make pcap_file=' + 'pcap_name' + '.pcap run-throughput')


def exp_run(number_of_times, workload, cc_alg_list, link_delays, link_bws, capture_on_switch=True, capture_as_text=False, run_throughput_graph=False, work_load_name='1', start_iperf=False, number_of_websites=None, time_slept=None):
    # log_file = open('logs1.log1', 'a')
    for cc_alg in cc_alg_list:
        for delay in link_delays:
            for bw in link_bws:
                for i in range(number_of_times):

                    name = work_load_name + '_' + str(len(workload)) + '_' + cc_alg + '_' + delay + '_' + bw + '_' + str(i)
                    if number_of_websites != None:
                        name = work_load_name + '_' + str(len(workload)) + '_' + cc_alg + '_' + delay + '_' + bw + '_' + str(number_of_websites) + '_' + str(time_slept)
                    setup_config_and_space(cc_alg=cc_alg, link_delay=delay, link_bw=bw)
                    # one time running end
                    # log_file.write(str(datetime.datetime.now()) + '\n')
                    run_all_experiments(workload, capture_on_switch, capture_as_text, capture_name=name, start_iperf=start_iperf)

                    if run_throughput_graph:
                        os.system('make pcap_file=' + name + '.pcap run-throughput')
    # log_file.close()



if __name__ == "__main__":
    number_of_websites = None
    # dirty
    time_slept = 25
    # dirty end
    if len(sys.argv) == 2:
        number_of_websites = int(sys.argv[1])
    global config
    running_exp = True
    capture_on_switch = True
    capture_as_text = False
    run_throughput_graph = False
    possible_applications = ['Web', 'Email', 'Vs', 'FTP', 'Vc']
    application_weights = [10, 17, 45, 15, 13]# [10, 7, 65, 5, 13] # boost of 10 and vs from 65 to 5, ftp from 3 to 5[0, 0, 100, 0, 0] https://www.sandvine.com/hubfs/Sandvine_Redesign_2019/Downloads/2023/reports/Sandvine%20GIPR%202023.pdf
    possible_clients = ['mn.client1', 'mn.client2', 'mn.client3', 'mn.client4']
    clients_weights = [25, 25, 25, 25]
    min_app_limits = [10, 10, 0, 1, 30]
    max_app_limits = [50, 100, 1, 5, 150]
    min_wait_time = 0.1
    max_wait_time = 15
    congestion_control_algorithm = 'cubic'  # 'reno' 'cubic' 'bbr'
    link_delays = ['1', '5', '10', '20', '30', '40', '50', '60', '75', '80']
    link_bws = ['5', '10', '20', '40', '60', '80', '100', '140', '180', '200']
    cc_alg_list = ['cubic', 'bbr', 'reno']
    repeat_for = 1
    number_of_different_workloads = 1
    number_of_tasks = 10
    start_iperf = False


    # # sleep 0.5, 1, 2
    # # link_bws '10', '100'
    # # background 10 - 1, 5, 10
    # # background 100 - 10, 50, 100
    # # change pcap as well
    #
    # link_bws = ['100']



    if number_of_websites is not None:
        min_app_limits = [number_of_websites, 10, 0, 5, 30]
        max_app_limits = [number_of_websites+1, 200, 1, 10, 150]

    if not running_exp:
        # starting main
        main(possible_applications, application_weights, possible_clients, clients_weights, number_of_tasks, min_app_limits, max_app_limits, min_wait_time, max_wait_time, capture_on_switch, capture_as_text, run_throughput_graph, cc_alg=congestion_control_algorithm)
    else:
        # log_file = open('logs.log', 'a')
        for num in range(number_of_different_workloads):
            workload = generate_workload(possible_applications, application_weights, possible_clients, clients_weights, number_of_tasks, min_app_limits, max_app_limits, min_wait_time, max_wait_time)
            # log_file.write(str(workload) + '\n')
            print(str(workload))
            if number_of_websites is not None:
                exp_run(repeat_for, workload, cc_alg_list, link_delays, link_bws, capture_on_switch, capture_as_text, run_throughput_graph, work_load_name=str(datetime.datetime.today().strftime('%Y%m%d%H%M')), start_iperf=start_iperf, number_of_websites=number_of_websites, time_slept=time_slept)
            else:
                exp_run(repeat_for, workload, cc_alg_list, link_delays, link_bws, capture_on_switch, capture_as_text, run_throughput_graph, work_load_name=str(datetime.datetime.today().strftime('%Y%m%d%H%M')), start_iperf=start_iperf)

        # log_file.close()