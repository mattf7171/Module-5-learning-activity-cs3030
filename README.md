Reflection:

I asked AI to help me design a small “Network Explorer Dashboard” that reports my hostname, local IP, public IP, and does quick HEAD requests for a few URLs. 
I refined its suggestions by keeping the script to one file, switching to HEAD for speed, and adding simple error labels like Timeout and ConnError so failures are easy to see. 
I learned how to get a reliable local IP using a UDP socket trick without actually sending data, and how to safely fetch a public IP from an API with a timeout. 
This exercise also showed me how small changes (like normalizing URLs and setting sensible defaults) make a CLI tool much nicer to use.
