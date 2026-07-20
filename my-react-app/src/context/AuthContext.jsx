import React, { createContext, useState, useContext, useEffect } from 'react';

const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [token, setToken] = useState(null);

  // Check for existing session on mount
  useEffect(() => {
    const initializeAuth = () => {
      try {
        const storedToken = localStorage.getItem('token');
        const storedUser = localStorage.getItem('user');
        
        console.log('Auth Init - storedToken:', storedToken);
        console.log('Auth Init - storedUser:', storedUser);
        
        if (storedToken && storedUser) {
          const parsedUser = JSON.parse(storedUser);
          setUser(parsedUser);
          setToken(storedToken);
          console.log('Auth Init - User restored:', parsedUser);
        } else {
          console.log('Auth Init - No stored session found');
        }
      } catch (error) {
        console.error('Error initializing auth:', error);
        localStorage.removeItem('token');
        localStorage.removeItem('user');
      } finally {
        setLoading(false);
      }
    };

    initializeAuth();
  }, []);

  const login = async (email, password) => {
  try {
    // For testing, you can change the role here
    const mockUser = {
      id: 1,
      name: 'Elton Mallya',
      email: 'test@example.com',
      role: 'admin', // Change to 'admin', 'staff', or 'customer' to test
      avatar: 'https://ui-avatars.com/api/?name=Elton+Mallya'
    };
    
    const mockToken = 'mock-jwt-token-' + Date.now();
    
    localStorage.setItem('token', mockToken);
    localStorage.setItem('user', JSON.stringify(mockUser));
    
    setUser(mockUser);
    setToken(mockToken);
    
    return { success: true, user: mockUser };
  } catch (error) {
    return { success: false, error: error.message };
  }
};
  const register = async (userData) => {
    try {
      console.log('Register attempt with:', userData);
      
      const mockUser = {
        id: Date.now(),
        name: userData.fullName,
        email: userData.email,
        phone: userData.phone,
        role: 'customer',
        avatar: `https://ui-avatars.com/api/?name=${encodeURIComponent(userData.fullName)}`
      };
      
      const mockToken = 'mock-jwt-token-' + Date.now();
      
      console.log('Register - Setting user:', mockUser);
      console.log('Register - Setting token:', mockToken);
      
      // Store in localStorage
      localStorage.setItem('token', mockToken);
      localStorage.setItem('user', JSON.stringify(mockUser));
      
      // Update state
      setUser(mockUser);
      setToken(mockToken);
      
      console.log('Register - State updated successfully');
      
      return { success: true, user: mockUser };
    } catch (error) {
      console.error('Register error:', error);
      return { success: false, error: error.message };
    }
  };

  const logout = () => {
    console.log('Logout - Clearing session');
    setUser(null);
    setToken(null);
    localStorage.removeItem('token');
    localStorage.removeItem('user');
  };

  const updateUser = (updatedData) => {
    if (user) {
      const updatedUser = { ...user, ...updatedData };
      setUser(updatedUser);
      localStorage.setItem('user', JSON.stringify(updatedUser));
      console.log('User updated:', updatedUser);
    }
  };

  // Compute isAuthenticated based on state
  const isAuthenticated = !!user && !!token;

  console.log('AuthContext - Current state:', { 
    user, 
    token, 
    loading, 
    isAuthenticated 
  });

  const value = {
    user,
    token,
    loading,
    login,
    register,
    logout,
    updateUser,
    isAuthenticated
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

export default AuthContext;