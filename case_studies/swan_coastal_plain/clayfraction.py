from scipy import special


def bore_to_fraction(interval_len, bore_dict):
    """
    convert a single bore hole log to clay fraction. the interval length in depth can be customized
    :param interval_len: length for a single interval
    :param bore_dict : a dict contains the lithology info, format: {(upper,lower): lithology_type}, the depth of bore
                        hole should be represented in AHD
    :return: a numeric list represents the clay fraction for the borehole
    """
    lower_list = [x[-1] for x in bore_dict.keys()]
    begin_of_depth = max([x[0] for x in bore_dict.keys()])
    end_of_depth = min(lower_list)
    interval_list = []
    upper_bound = begin_of_depth
    lower_bound = interval_len* (begin_of_depth//interval_len)
    while lower_bound >= end_of_depth:
        interval_list.append((upper_bound, lower_bound))
        upper_bound = lower_bound
        lower_bound = lower_bound- interval_len
        if lower_bound < end_of_depth:
            interval_list.append((upper_bound, end_of_depth))
            break
    print(interval_list)
    fraction_dict={}
    for interval in interval_list:
        fraction_dict[interval] = get_fraction(interval,bore_dict)
    return fraction_dict


def get_fraction(interval,bore_dict):
    """
    calculate the clay fraction for a borehole.
    :param interval: a tuple (from_depth, to_depth )
    :param bore_dict: dictionary {(from_depth, to_depth): lithology_type}
    :return: clay fraction for a bore hole in a specific interval
    """
    clay_amount = 0
    interval_len = interval[0]-interval[1]
    for bore_depth in bore_dict.keys():
        if bore_dict[bore_depth] =="clay":
            if bore_depth[0] >= interval[0] and bore_depth[1] <= interval[1]: # cover the whole interval
                clay_amount = interval_len
                break
            elif bore_depth[1] >= interval[0] or bore_depth[0] <= interval[1]:  # this segment is not in the interval
                continue
            elif bore_depth[0] <= interval[0] and bore_depth[1] >= interval[1]:  # inside the interval
                clay_amount = clay_amount+(bore_depth[0]-bore_depth[1])
                continue
            elif bore_depth[0] <= interval[0] and bore_depth[1] <= interval[1]:  # partially overlapping, upper part of borehole is overlapping
                clay_amount = clay_amount + (bore_depth[0]-interval[1])
                continue
            else:
                clay_amount += (interval[0]-bore_depth[1])
    return clay_amount/interval_len


def resist_to_fraction(interval, resist_dict, translator_function,training = False, m_low= 40, m_up= 70):
    """
    calculate clay fraction with resistivity data for a specific location
    :param interval: a tuple (from_depth, to_depth)
    :param resist_dict: dictionary {(from_depth, to_depth): resistivity}
    :param translator_function: translator function (W(r)) for a specific grid. The value for W(r) is weight, r is the
            resistivity.
    :param training: if it is training parameters (m_up and m_low), by default it is false
    :param m_up and m_low: parameters for translator function. By default, m_low =40 and m_up = 70
    :return: clay fraction for a specific location in a certain interval
    """
    res = 0
    interval_len = interval[1] - interval[0]
    for layer in resist_dict.keys():
        thickness = overlap(layer, interval)
        if thickness != 0:
            if not training:
                res = res + translator_function(resist_dict[layer])*thickness
            else:
                res = res + translator_function(resist_dict[layer],m_low,m_up) * thickness
    res = res / interval_len
    return res


def translator_function (resistivity, m_low= 40, m_up= 70):
    """
    calculate the value of translator function given a resistivity. The translator function is a complementary error
    function. m_low is the resistivity when weight is 97.5% (almost clay), m_up is the resistivity when weight is 2.5%
    (almost sand).
    :param resistivity:
    :param m_low: 40 by default
    :param m_up: 70 by default
    :return:
    """
    weight = 0
    k = special.erfcinv(0.05)
    x = (2*resistivity-m_up-m_low)/(m_up-m_low)
    weight = 0.5 * special.erfc(k*x)
    return weight


def overlap(layer, interval):
    """
    calculate the thickness for a layer that overlapping with an interval
    :param layer: (from_depth, to_depth)
    :param interval: (from_depth, to_depth)
    :return: the overlapping thickness
    """
    res = 0
    if layer[0] >= interval[0] and layer[1] <= interval[1]:  # cover the whole interval
        res = interval[1] - interval[0]
    elif layer[1] >= interval[0] or layer[0] <= interval[1]:  # this segment is not in the interval
        pass
    elif layer[0] <= interval[0] and layer[1] >= interval[1]:  # inside the interval
        res = layer[1]-layer[0]
    elif layer[0] >= interval[0] and layer[1] >= interval[1]: # lower part of the layer is overlapped
        res = interval[0] - layer[1]
    else:
        res = layer[0] - interval[1]
    return res
