export const generateSampleCSV = () => {
    const rows = [['ds', 'y']];
    const startDate = new Date();
    startDate.setDate(startDate.getDate() - 100);

    let val = 15000;
    for (let i = 0; i < 100; i++) {
        const date = new Date(startDate);
        date.setDate(date.getDate() + i);

        // Add some "cool" trend and seasonality
        val += (Math.random() * 100 - 45) + (Math.sin(i / 5) * 50);
        rows.push([date.toISOString().split('T')[0], val.toFixed(2)]);
    }

    return rows.map(r => r.join(',')).join('\n');
};

export const getSampleFile = () => {
    const csvContent = generateSampleCSV();
    const blob = new Blob([csvContent], { type: 'text/csv' });
    return new File([blob], 'nifty_sample_data.csv', { type: 'text/csv' });
};
