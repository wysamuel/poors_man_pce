import cmd,os,zmq,pickle,argparse,sys,os


class PceShell(cmd.Cmd):
    def __init__(self,**kwargs):

        self.client_port = "5559"
        self.server_port = "5557"
        self.client_context=zmq.Context()
        self.server_context=zmq.Context()
        self.client_socket=self.client_context.socket(zmq.REQ)
        self.client_socket.connect("tcp://localhost:%s" % self.client_port)
        self.server_socket = self.server_context.socket(zmq.REP)
        self.server_socket.bind("tcp://*:%s" % self.server_port)
        self.code_check_node = "check_node"
        self.code_show_nodes = "show_nodes"
        self.code_run_spf = "run_spf"
        self.code_run_spf_avoid_node="run_spf_avoid_node"
        self.code_run_spf_avoid_node_color="run_spf_avoid_node_color"
        self.code_run_spf_avoid_color="run_spf_avoid_color"
        super().__init__()

    def show_nodes(self):
        """shows all the nodes in the topology"""
        print ("Grabbing the topology details")
        pobj_send= pickle.dumps(self.code_show_nodes,3)
        self.client_socket.send(pobj_send)

        pobj_recv=self.client_socket.recv()
        print ("The Nodes are",pickle.loads(pobj_recv))

    def check_nodes(self,node_name):
        check_node = self.code_check_node+" "+ node_name
        pobj_send=pickle.dumps(check_node)
        self.client_socket.send(pobj_send)
        pobj_recv=self.client_socket.recv()
        result = pickle.loads(pobj_recv)

        return result

    def run_spf(self,nodes,avoid=None,link_color=None):
        """ Find the shortest path between nodes A and B and Optionally Avoid node C if given"""
        #print ("Enter the Node A and B ")
        if avoid is None and link_color is None:
            print ("Shortest Path between {}".format(','.join(nodes)))
            """Check if the Nodes are Valid nodes in the topology"""
            for node in nodes:
                result = self.check_nodes(node)
                if result is False:
                    print ("Its an Invalid Node.Please enter a valid node from Topology")
                    os._exit(1)
            request_spf = self.code_run_spf +" "+nodes[0]+" "+nodes[1]
            pobj_send = pickle.dumps(request_spf)
            self.client_socket.send(pobj_send)
            pobj_recv = self.client_socket.recv()
            path_list = pickle.loads(pobj_recv)
            if path_list:
                for path in path_list:
                    print ("Paths are ",path)
            else:
                print ("No Paths found")
        elif avoid is not None and link_color is None:
            print ("Finding Shortest Path between {} and Avoiding {} ".format(','.join(nodes),','.join(avoid)))
            for node in nodes:
                result = self.check_nodes(node)
                if result is False:
                    print ("Its an Invalid Node.Please enter a valid node from Topology")
                    os._exit(1)
            for node in avoid:
                result = self.check_nodes(node)
                if result is False:
                    print ("Its an Invalid Node.Please enter a valid node from Topology")
                    os._exit(1)

            avoid_node = str()
            for node in avoid:
                avoid_node= avoid_node+" "+ node

            request_spf = self.code_run_spf_avoid_node+" "+nodes[0]+" "+nodes[1]+avoid_node
            pobj_send = pickle.dumps(request_spf)
            self.client_socket.send(pobj_send)
            pobj_recv = self.client_socket.recv()
            path_list = pickle.loads(pobj_recv)
            if path_list:
                for path in path_list:
                    print ("Paths are ",path)
            else:
                print ("No Paths found")

        elif avoid is not None and link_color is not None:
            print ("Finding Shortest Path between {} and Avoiding nodes {} and {} color {} ".format(','.join(nodes),','.join(avoid),link_color[0],link_color[1]))
            for node in nodes:
                result = self.check_nodes(node)
                if result is False:
                    print ("Its an Invalid Node.Please enter a valid node from Topology")
                    os._exit(1)
            for node in avoid:
                result = self.check_nodes(node)
                if result is False:
                    print ("Its an Invalid Node.Please enter a valid node from Topology")
                    os._exit(1)

            avoid_node = str()
            for node in avoid:
                avoid_node= avoid_node+" "+ node

            request_spf = self.code_run_spf_avoid_node_color+" "+nodes[0]+" "+nodes[1]+avoid_node+" "+link_color[0]+" "+link_color[1]
            pobj_send = pickle.dumps(request_spf)
            self.client_socket.send(pobj_send)
            pobj_recv = self.client_socket.recv()
            path_list = pickle.loads(pobj_recv)
            if path_list:
                for path in path_list:
                    print ("Paths are ",path)
            else:
                print ("No Paths found")

        elif avoid is None and link_color is not None:
            print ("looking for Shortest Path between {} and {} color {} ".format(','.join(nodes),link_color[0],link_color[1]))
            for node in nodes:
                result = self.check_nodes(node)
                if result is False:
                    print ("Its an Invalid Node.Please enter a valid node from Topology")
                    os._exit(1)

            request_spf = self.code_run_spf_avoid_color+" "+nodes[0]+" "+nodes[1]+" "+link_color[0]+" "+link_color[1]
            pobj_send = pickle.dumps(request_spf)
            self.client_socket.send(pobj_send)
            pobj_recv = self.client_socket.recv()
            path_list = pickle.loads(pobj_recv)
            if path_list:
                for path in path_list:
                    print ("Paths are ",path)
            else:
                print ("No Paths found")


def main():
    pceshell=PceShell()
    pce_parser=argparse.ArgumentParser(description='PCE Cmd Line Options')

    pce_subparser=pce_parser.add_subparsers(help='Find CSPF',dest='mode')

    pce_parser.add_argument('--show_nodes','-sn',action='store_true',help='Shows Node Names present in the topology')

    findcspf_parser=pce_subparser.add_parser('cspf',help='Find CSPF between Node A and B')
    findcspf_parser.add_argument('--find_spf','-spf',nargs=2,metavar=('src_node','dst_node'),help='Find CSPF between Nodes A and B')
    findcspf_parser.add_argument('--avoid','-a',nargs='+',help='Avoid these nodes')
    findcspf_parser.add_argument('--link_color','-lc',nargs=2,metavar=('exclude_include','color'),help='Please use "exclude" or "include" and then color ex: "blue" ')

    args=pce_parser.parse_args()
    print ("NameSpace :",args)
    if args.show_nodes:
        print ("Nodes are",pceshell.show_nodes())
    elif args.mode == "cspf":
        if args.avoid and args.link_color:
            print (pceshell.run_spf(args.find_spf,args.avoid,link_color=args.link_color))
        elif args.avoid:
            print (pceshell.run_spf(args.find_spf,args.avoid))
        elif args.link_color:
            print (pceshell.run_spf(args.find_spf,link_color=args.link_color))
        else:
            print (pceshell.run_spf(args.find_spf))

if __name__=='__main__':
    main()


