import mongoose from 'mongoose';

const symptomSchema = new mongoose.Schema(
  {
    userId: {
      type: mongoose.Schema.Types.ObjectId,
      ref: 'User', // Reference to User model
      required: [true, 'User ID is required']
    },
    date: {
      type: Date,
      required: [true, 'Please provide a date']
    },
    symptoms: {
      type: [String], // Array of symptom strings
      default: [],
      validate: {
        validator: function (v) {
          return v.length <= 10; // Max 10 symptoms per entry
        },
        message: 'You can log maximum 10 symptoms'
      }
    },
    mood: {
      type: String,
      enum: ['happy', 'sad', 'neutral', 'anxious', 'irritable', 'excited'],
      default: 'neutral'
    },
    energy: {
      type: String,
      enum: ['low', 'medium', 'high'],
      default: 'medium'
    },
    notes: {
      type: String,
      maxlength: [500, 'Notes cannot exceed 500 characters'],
      default: ''
    }
  },
  { timestamps: true }
);

const Symptom = mongoose.model('Symptom', symptomSchema);

export default Symptom;
