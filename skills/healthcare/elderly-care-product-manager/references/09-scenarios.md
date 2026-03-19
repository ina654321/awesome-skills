# Scenario Examples

## 9.1 Fall Prevention Device Design

**User:** "We're designing a smart watch for elderly users that monitors for falls and alerts caregivers. What key considerations should we address in the design requirements?"

**Expert:**
> **Analysis:**
>
> **User Needs Assessment:**
> ```
> Primary: Reliable fall detection without false alarms
> Secondary: Easy to wear, comfortable battery life
> Tertiary: Discreet appearance, affordable
> ```
>
> **Critical Design Requirements:**
> 1. **Detection Accuracy**: >95% sensitivity, <5% false positive rate
> 2. **Latency**: Alert within 60 seconds of fall
> 3. **Battery**: Minimum 3-day life with daily charging reminder
> 4. **Interface**: Large SOS button, simple pairing
>
> **Use-Related Risk Scenarios:**
> - False negative: Fall not detected → Injury worsens
> - False positive: Unnecessary emergency response
> - Use error: Unable to cancel false alarm
>
> **Mitigations:**
> ```
> • Algorithmic detection (accelerometer + gyroscope)
> • "I'm okay" confirmation button
> • Automatic escalation after 60 seconds
> • Caregiver app with response tracking
> • Periodic self-test reminder
> ```
>
> **Accessibility Compliance:**
> - Visual: High contrast display, adjustable text
> - Motor: Large touch targets, haptic feedback
> - Cognitive: Simple interface, audio prompts
> - Auditory: Vibration + visual + audio alerts

## 9.2 Medication Management App

**User:** "Our startup wants to develop a medication reminder app for seniors. What features should we prioritize and what regulatory considerations apply?"

**Expert:**
> **Analysis:**
>
> **Priority Features:**
> ```
> 1. Simple medication entry (scan or manual)
> 2. Visual and audio reminders with large text
> 3. Caregiver notification system
> 4. Adherence tracking and reporting
> 5. Refill reminders
> ```
>
> **Regulatory Consideration:**
> - General wellness app (Class I) - no FDA clearance needed
> - If claims for diagnosis/treatment → Class II/III
> - Must NOT claim to detect drug interactions without proper validation
>
> **Design for Seniors:**
> - Large, high-contrast buttons
> - Simple navigation (max 2 taps to action)
> - Optional family/caregiver view
> - Offline functionality
> - Voice input option
>
> **Clinical Validation:**
> - Test with >50 elderly users across demographics
> - Include users with mild cognitive impairment
> - Validate under actual use conditions
> - Document all use errors
