def calculate_RTTs(sample_rtts, estimated_rtt, dev_rtt, alpha, beta):
    results = []
    for i, sample_rtt in enumerate(sample_rtts, 1):
        new_estimated_rtt = (1 - alpha) * estimated_rtt + alpha * sample_rtt
        new_dev_rtt = (1 - beta) * dev_rtt + beta * abs(sample_rtt - new_estimated_rtt)
        timeout_interval = new_estimated_rtt + 4 * new_dev_rtt
        
        results.append((round(new_estimated_rtt, 2), round(new_dev_rtt, 2), round(timeout_interval, 2)))
        
        print()
        print(f'Nach dem {i}-ten SampleRTT ({sample_rtt} ms):')
        print(f'EstimatedRTT = (1 - {alpha}) * {round(estimated_rtt, 2)} ms + {alpha} * {sample_rtt} ms = {round(new_estimated_rtt, 2)} ms')
        print(f'DevRTT = (1 - {beta}) * {round(dev_rtt, 2)} ms + {beta} * |{sample_rtt} ms - {round(new_estimated_rtt, 2)} ms| = {round(new_dev_rtt, 2)} ms')
        print(f'TimeOutInterval = {round(new_estimated_rtt, 2)} ms + 4 * {round(new_dev_rtt, 2)} ms = {round(timeout_interval, 2)} ms')

        estimated_rtt = new_estimated_rtt
        dev_rtt = new_dev_rtt
    return results

alpha = 0.125
beta = 0.25
sample_rtts = [106, 120, 140, 90]
initial_estimated_rtt = 100
initial_dev_rtt = 5

rtts = calculate_RTTs(sample_rtts, initial_estimated_rtt, initial_dev_rtt, alpha, beta)