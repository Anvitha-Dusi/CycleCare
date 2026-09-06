import mongoose from 'mongoose';

const periodSchema = new mongoose.Schema(
  {
    userId: {
      type: mongoose.Schema.Types.ObjectId,
      ref: 'User', // Reference to User model
      required: [true, 'User ID is required']
    },
    startDate: {
      type: Date,
      required: [true, 'Please provide a start date']
    },
    endDate: {
      type: Date,
      default: null // Optional - user might not have ended period yet
    },
    flow: {
      type: String,
      enum: ['light', 'moderate', 'heavy'],
      default: 'moderate'
    },
    notes: {
      type: String,
      maxlength: [500, 'Notes cannot exceed 500 characters'],
      default: ''
    }
  },
  { timestamps: true }
);

const Period = mongoose.model('Period', periodSchema);

export default Period;
