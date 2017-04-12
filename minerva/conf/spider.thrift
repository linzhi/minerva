service SpiderService {
    string send_url();
    bool receive_url(1: set<string> urls);
}

