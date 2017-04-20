service SpiderService {
    string send_url(1: string url_type);
    bool receive_url(1: set<string> urls, 2: string url_type);
}

