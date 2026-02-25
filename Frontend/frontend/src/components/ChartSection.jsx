import React from 'react';
import LearningLevelChart from './Charts/LearningLevelChart';

const ChartSection = ({ data }) => {
    return (
        <div className="charts-grid">
            <LearningLevelChart data={data} />
            {/* Extended: Space for other charts if needed, e.g. Attendance Weekly Trend */}
        </div>
    );
};

export default ChartSection;
