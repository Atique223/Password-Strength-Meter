import re
import streamlit as st

class PasswordStrengthMeter:
    def __init__(self):
        # Minimum requirements
        self.min_length = 8
        self.max_length = 64

    def evaluate_strength(self, password):
        """
        Evaluate password strength based on multiple criteria
        Returns a dictionary with strength details
        """
        # Handle empty password
        if not password:
            return {
                'length': 0,
                'uppercase': 0,
                'lowercase': 0,
                'numbers': 0,
                'special_chars': 0,
                'complexity_score': 0,
                'strength_label': 'No Password Entered',
                'color': 'gray'
            }

        # Initialize strength metrics
        strength_metrics = {
            'length': self._check_length(password),
            'uppercase': self._has_uppercase(password),
            'lowercase': self._has_lowercase(password),
            'numbers': self._has_numbers(password),
            'special_chars': self._has_special_chars(password),
            'complexity_score': 0,
            'strength_label': 'Very Weak'
        }

        # Calculate complexity score
        complexity_score = sum([
            strength_metrics['length'],
            strength_metrics['uppercase'],
            strength_metrics['lowercase'],
            strength_metrics['numbers'],
            strength_metrics['special_chars']
        ])
        strength_metrics['complexity_score'] = complexity_score

        # Determine strength label
        if complexity_score <= 2:
            strength_metrics['strength_label'] = 'Very Weak'
            strength_metrics['color'] = 'red'
        elif complexity_score <= 4:
            strength_metrics['strength_label'] = 'Weak'
            strength_metrics['color'] = 'orange'
        elif complexity_score <= 6:
            strength_metrics['strength_label'] = 'Moderate'
            strength_metrics['color'] = 'yellow'
        elif complexity_score <= 8:
            strength_metrics['strength_label'] = 'Strong'
            strength_metrics['color'] = 'green'
        else:
            strength_metrics['strength_label'] = 'Very Strong'
            strength_metrics['color'] = 'darkgreen'

        return strength_metrics

    def _check_length(self, password):
        """Check password length"""
        if len(password) < self.min_length:
            return 0
        elif len(password) > self.max_length:
            return 1
        else:
            return 2

    def _has_uppercase(self, password):
        """Check for uppercase letters"""
        return 1 if re.search(r'[A-Z]', password) else 0

    def _has_lowercase(self, password):
        """Check for lowercase letters"""
        return 1 if re.search(r'[a-z]', password) else 0

    def _has_numbers(self, password):
        """Check for numeric characters"""
        return 1 if re.search(r'\d', password) else 0

    def _has_special_chars(self, password):
        """Check for special characters"""
        return 1 if re.search(r'[!@#$%^&*(),.?":{}|<>]', password) else 0

def streamlit_app():
    """
    Streamlit application for password strength meter
    """
    # Set page title and icon
    st.set_page_config(page_title="Password Strength Meter", page_icon="🔐")
    
    # Title and description
    st.title("🔐 Password Strength Meter")
    st.markdown("Check the strength of your password in real-time!")
    
    # Initialize password strength meter
    psm = PasswordStrengthMeter()
    
    # Create a form for better user interaction
    with st.form(key='password_strength_form'):
        # Password input
        password = st.text_input("Enter your password", type="password", 
                                 help="Your password will not be stored or shared")
        
        # Check Strength button
        check_strength = st.form_submit_button("Check Strength 💪")
    
    # Analyze password when button is clicked
    if check_strength:
        # Evaluate password strength
        result = psm.evaluate_strength(password)
        
        # Display strength label with color
        st.markdown(f"**Strength:** <span style='color:{result['color']}'>{result['strength_label']}</span>", 
                    unsafe_allow_html=True)
        
        # Progress bar for complexity
        st.progress(result['complexity_score'] / 10)
        
        # Detailed breakdown
        st.subheader("Strength Criteria")
        
        # Create columns for criteria
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f"**Length:** {'✓' if result['length'] > 0 else '✗'}")
            st.markdown(f"**Uppercase Letters:** {'✓' if result['uppercase'] > 0 else '✗'}")
        
        with col2:
            st.markdown(f"**Lowercase Letters:** {'✓' if result['lowercase'] > 0 else '✗'}")
            st.markdown(f"**Numbers:** {'✓' if result['numbers'] > 0 else '✗'}")
        
        # Special characters in a separate row
        st.markdown(f"**Special Characters:** {'✓' if result['special_chars'] > 0 else '✗'}")
        
        # Password strength tips
        st.subheader("Tips for a Strong Password")
        tips = [
            "Use at least 8 characters",
            "Include uppercase and lowercase letters",
            "Add numbers and special characters",
            "Avoid common words or patterns",
            "Use a unique password for each account"
        ]
        for tip in tips:
            st.markdown(f"- {tip}")

def main():
    # CLI interface (optional, can be removed if only using Streamlit)
    psm = PasswordStrengthMeter()
    
    while True:
        password = input("Enter a password to check its strength (or 'q' to quit): ")
        
        if password.lower() == 'q':
            break
        
        result = psm.evaluate_strength(password)
        
        print("\nPassword Strength Analysis:")
        print(f"Strength Label: {result['strength_label']}")
        print(f"Complexity Score: {result['complexity_score']}/10")
        print("\nDetailed Breakdown:")
        print(f"Length Check: {'✓' if result['length'] > 0 else '✗'}")
        print(f"Uppercase Letters: {'✓' if result['uppercase'] > 0 else '✗'}")
        print(f"Lowercase Letters: {'✓' if result['lowercase'] > 0 else '✗'}")
        print(f"Numbers: {'✓' if result['numbers'] > 0 else '✗'}")
        print(f"Special Characters: {'✓' if result['special_chars'] > 0 else '✗'}")

if __name__ == '__main__':
    # Uncomment the appropriate line based on how you want to run the app
    # main()  # For CLI interface
    streamlit_app()  # For Streamlit web app