import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { 
  Search, 
  Send, 
  Paperclip, 
  Image,
  Smile,
  MoreVertical,
  Phone,
  Video,
  User,
  Clock,
  CheckCheck,
  Check,
  MessageSquare
} from 'lucide-react';
import MainLayout from '../../layouts/MainLayout';

const Messages = () => {
  const [conversations, setConversations] = useState([]);
  const [selectedConversation, setSelectedConversation] = useState(null);
  const [messages, setMessages] = useState([]);
  const [newMessage, setNewMessage] = useState('');
  const [searchTerm, setSearchTerm] = useState('');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Fetch conversations
    const fetchConversations = async () => {
      try {
        // Mock data
        setConversations([
          {
            id: 1,
            name: 'Support Team',
            avatar: 'https://ui-avatars.com/api/?name=Support+Team',
            lastMessage: 'We are looking into your issue. Our team will contact you shortly.',
            timestamp: '2025-06-08T14:20:00Z',
            unread: 2,
            online: true,
            isStaff: true
          },
          {
            id: 2,
            name: 'Billing Department',
            avatar: 'https://ui-avatars.com/api/?name=Billing+Dept',
            lastMessage: 'Your invoice has been corrected. Please check your email.',
            timestamp: '2025-06-07T16:45:00Z',
            unread: 0,
            online: false,
            isStaff: true
          },
          {
            id: 3,
            name: 'Technical Support',
            avatar: 'https://ui-avatars.com/api/?name=Tech+Support',
            lastMessage: 'We have scheduled a technician visit for tomorrow.',
            timestamp: '2025-06-06T10:30:00Z',
            unread: 1,
            online: true,
            isStaff: true
          }
        ]);
        
        // Select first conversation
        setSelectedConversation(1);
      } catch (error) {
        console.error('Error fetching conversations:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchConversations();
  }, []);

  useEffect(() => {
    // Fetch messages for selected conversation
    if (selectedConversation) {
      const fetchMessages = async () => {
        try {
          // Mock messages
          setMessages([
            {
              id: 1,
              sender: 'staff',
              senderName: 'Support Team',
              message: 'Hello! How can we help you today?',
              timestamp: '2025-06-08T13:00:00Z',
              read: true
            },
            {
              id: 2,
              sender: 'user',
              senderName: 'You',
              message: 'I have an issue with my internet connection. It keeps dropping every 30 minutes.',
              timestamp: '2025-06-08T13:05:00Z',
              read: true
            },
            {
              id: 3,
              sender: 'staff',
              senderName: 'Support Team',
              message: 'I understand. Let me check your account. Could you please confirm your account number?',
              timestamp: '2025-06-08T13:15:00Z',
              read: true
            },
            {
              id: 4,
              sender: 'user',
              senderName: 'You',
              message: 'My account number is ACC-2025-001234.',
              timestamp: '2025-06-08T13:20:00Z',
              read: true
            },
            {
              id: 5,
              sender: 'staff',
              senderName: 'Support Team',
              message: 'Thank you. I can see the issue now. We will need to reset your connection from our end. This should be resolved in 15 minutes.',
              timestamp: '2025-06-08T14:15:00Z',
              read: false
            }
          ]);
        } catch (error) {
          console.error('Error fetching messages:', error);
        }
      };

      fetchMessages();
    }
  }, [selectedConversation]);

  const filteredConversations = conversations.filter(conv =>
    conv.name.toLowerCase().includes(searchTerm.toLowerCase())
  );

  const formatTimestamp = (timestamp) => {
    const date = new Date(timestamp);
    const now = new Date();
    const diffHours = (now - date) / (1000 * 60 * 60);
    
    if (diffHours < 1) {
      return `${Math.floor(diffHours * 60)}m ago`;
    } else if (diffHours < 24) {
      return `${Math.floor(diffHours)}h ago`;
    } else {
      return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
    }
  };

  const getTimeDisplay = (timestamp) => {
    const date = new Date(timestamp);
    return date.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' });
  };

  const handleSendMessage = (e) => {
    e.preventDefault();
    if (!newMessage.trim()) return;

    const newMsg = {
      id: messages.length + 1,
      sender: 'user',
      senderName: 'You',
      message: newMessage,
      timestamp: new Date().toISOString(),
      read: true
    };

    setMessages([...messages, newMsg]);
    setNewMessage('');
  };

  const getConversation = (id) => {
    return conversations.find(c => c.id === id);
  };

  const selectedConv = getConversation(selectedConversation);

  const containerVariants = {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: {
        staggerChildren: 0.1
      }
    }
  };

  const itemVariants = {
    hidden: { y: 20, opacity: 0 },
    visible: {
      y: 0,
      opacity: 1
    }
  };

  return (
    <MainLayout>
      <motion.div
        initial="hidden"
        animate="visible"
        variants={containerVariants}
        className="p-4 p-md-5"
      >
        {/* Header */}
        <motion.div variants={itemVariants} className="mb-4">
          <h2 className="fw-bold mb-1">Messages</h2>
          <p className="text-muted">Chat with our support team</p>
        </motion.div>

        {/* Messages Container */}
        <motion.div variants={itemVariants}>
          <div className="card card-custom p-0 overflow-hidden">
            <div className="row g-0" style={{ minHeight: '600px' }}>
              {/* Conversations List */}
              <div className="col-12 col-md-4 border-end">
                <div className="p-3 border-bottom">
                  <div className="position-relative">
                    <Search size={18} className="position-absolute text-muted" style={{ left: '12px', top: '50%', transform: 'translateY(-50%)' }} />
                    <input
                      type="text"
                      className="form-control ps-5"
                      placeholder="Search conversations..."
                      value={searchTerm}
                      onChange={(e) => setSearchTerm(e.target.value)}
                    />
                  </div>
                </div>

                <div className="overflow-auto" style={{ maxHeight: '500px' }}>
                  {filteredConversations.map((conv) => (
                    <div
                      key={conv.id}
                      className={`p-3 border-bottom cursor-pointer hover-lift ${selectedConversation === conv.id ? 'bg-light' : ''}`}
                      onClick={() => setSelectedConversation(conv.id)}
                    >
                      <div className="d-flex align-items-center gap-3">
                        <img
                          src={conv.avatar}
                          alt={conv.name}
                          className="rounded-circle"
                          width={48}
                          height={48}
                        />
                        <div className="flex-grow-1 overflow-hidden">
                          <div className="d-flex justify-content-between align-items-center">
                            <h6 className="fw-bold mb-0 text-truncate">{conv.name}</h6>
                            <span className="text-muted small flex-shrink-0">
                              {formatTimestamp(conv.timestamp)}
                            </span>
                          </div>
                          <div className="d-flex justify-content-between align-items-center">
                            <p className="text-muted small text-truncate mb-0" style={{ maxWidth: '150px' }}>
                              {conv.lastMessage}
                            </p>
                            {conv.unread > 0 && (
                              <span className="badge bg-primary rounded-circle">
                                {conv.unread}
                              </span>
                            )}
                          </div>
                          {conv.online && (
                            <span className="small text-success d-flex align-items-center gap-1">
                              <span className="bg-success rounded-circle d-inline-block" style={{ width: '6px', height: '6px' }} />
                              Online
                            </span>
                          )}
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>

              {/* Chat Area */}
              <div className="col-12 col-md-8 d-flex flex-column">
                {selectedConv ? (
                  <>
                    {/* Chat Header */}
                    <div className="p-3 border-bottom d-flex justify-content-between align-items-center">
                      <div className="d-flex align-items-center gap-3">
                        <img
                          src={selectedConv.avatar}
                          alt={selectedConv.name}
                          className="rounded-circle"
                          width={40}
                          height={40}
                        />
                        <div>
                          <h6 className="fw-bold mb-0">{selectedConv.name}</h6>
                          {selectedConv.online && (
                            <span className="small text-success">Online</span>
                          )}
                        </div>
                      </div>
                      <div className="d-flex gap-2">
                        <button className="btn btn-outline-secondary btn-sm d-flex align-items-center gap-1">
                          <Phone size={16} />
                        </button>
                        <button className="btn btn-outline-secondary btn-sm d-flex align-items-center gap-1">
                          <Video size={16} />
                        </button>
                        <button className="btn btn-outline-secondary btn-sm">
                          <MoreVertical size={16} />
                        </button>
                      </div>
                    </div>

                    {/* Messages */}
                    <div className="flex-grow-1 overflow-auto p-3" style={{ maxHeight: '400px', backgroundColor: '#f8f9fa' }}>
                      {messages.map((msg, index) => (
                        <div
                          key={msg.id}
                          className={`d-flex ${msg.sender === 'user' ? 'justify-content-end' : 'justify-content-start'} mb-3`}
                        >
                          <div className={`max-width-75 ${msg.sender === 'user' ? 'order-2' : 'order-1'}`}>
                            <div
                              className={`p-3 rounded-3 ${
                                msg.sender === 'user'
                                  ? 'bg-primary text-white'
                                  : 'bg-white'
                              }`}
                              style={{ maxWidth: '75%' }}
                            >
                              <p className="mb-1">{msg.message}</p>
                              <div className="d-flex align-items-center justify-content-end gap-1">
                                <span className={`small ${msg.sender === 'user' ? 'text-white-50' : 'text-muted'}`}>
                                  {getTimeDisplay(msg.timestamp)}
                                </span>
                                {msg.sender === 'user' && (
                                  msg.read ? (
                                    <CheckCheck size={14} className="text-white-50" />
                                  ) : (
                                    <Check size={14} className="text-white-50" />
                                  )
                                )}
                              </div>
                            </div>
                          </div>
                        </div>
                      ))}
                    </div>

                    {/* Message Input */}
                    <div className="p-3 border-top bg-white">
                      <form onSubmit={handleSendMessage} className="d-flex gap-2">
                        <button type="button" className="btn btn-link text-muted p-0">
                          <Paperclip size={20} />
                        </button>
                        <button type="button" className="btn btn-link text-muted p-0">
                          <Image size={20} />
                        </button>
                        <input
                          type="text"
                          className="form-control flex-grow-1"
                          placeholder="Type a message..."
                          value={newMessage}
                          onChange={(e) => setNewMessage(e.target.value)}
                        />
                        <button type="button" className="btn btn-link text-muted p-0">
                          <Smile size={20} />
                        </button>
                        <button type="submit" className="btn btn-primary d-flex align-items-center gap-1">
                          <Send size={18} />
                        </button>
                      </form>
                    </div>
                  </>
                ) : (
                  <div className="d-flex align-items-center justify-content-center flex-grow-1 p-5">
                    <div className="text-center">
                      <MessageSquare size={48} className="text-muted mb-3" />
                      <h6 className="fw-bold">Select a conversation</h6>
                      <p className="text-muted small">Choose a conversation from the list to start chatting</p>
                    </div>
                  </div>
                )}
              </div>
            </div>
          </div>
        </motion.div>
      </motion.div>
    </MainLayout>
  );
};

export default Messages;