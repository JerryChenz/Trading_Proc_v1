import smart_value


def update_monitor():
    """Update the pipeline monitor"""

    o = smart_value.tools.monitor.Monitor()
    o.load_opportunities()

if __name__ == '__main__':
    update_monitor()