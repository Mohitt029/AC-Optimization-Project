% Load and visualize simulation results
data = readtable('C:/Users/HP/OneDrive/Desktop/AC_Simulator/results/simulation_results.csv');
if isempty(data)
    error('Simulation results CSV is empty or not found.');
end

% Debug: Print column names
disp('Column names in data:');
disp(data.Properties.VariableNames);

% Extract data
time = data{:, 'Time_min_'};
orig_temp = data{:, 'OriginalTemp___C_'};
adj_temp = data{:, 'AdjustedTemp___C_'};
settings = data{:, 'Setting'};
energy = data{:, 'EnergyUsage'};

% Validate data
if isempty(time) || isempty(orig_temp) || isempty(adj_temp) || isempty(energy)
    error('One or more data arrays are empty.');
end

% Calculate additional metrics
total_energy = sum(energy) * (1440 / length(energy)); % Total energy for 24 hours
baseline_energy = 1500; % Hypothetical baseline (e.g., constant AC)
energy_saving = (baseline_energy - total_energy) / baseline_energy * 100;
comfort_zone = mean(adj_temp >= 22 & adj_temp <= 24) * 100; % % time in 22-24°C
settings_cat = categorical(settings); % Convert to categorical
setting_counts = countcats(settings_cat); % Count occurrences of each category
setting_freq = (setting_counts / sum(setting_counts)) * 100; % % of each setting
temp_deviation = orig_temp - adj_temp; % Cooling effect

% Display insights
fprintf('Analysis Results:\n');
fprintf('Total Energy Used: %.2f units\n', total_energy);
fprintf('Energy Saving vs Baseline: %.2f%%\n', energy_saving);
fprintf('Comfort Zone (22-24°C): %.2f%%\n', comfort_zone);
unique_settings = unique(settings);
fprintf('Setting Frequencies: ');
for i = 1:length(unique_settings)
    fprintf('%s %.2f%%, ', unique_settings{i}, setting_freq(i));
end
fprintf('\n');

% Figure 1: Temperature Optimization
figure('Position', [100, 100, 600, 400]);
h1 = plot(time, orig_temp, 'b-', 'LineWidth', 2, 'DisplayName', 'Original Temp');
hold on;
h2 = plot(time, adj_temp, 'r-', 'LineWidth', 2, 'DisplayName', 'Adjusted Temp');
title('Temperature Optimization Over 24 Hours');
xlabel('Time (minutes)');
ylabel('Temperature (°C)');
legend([h1, h2], {'Original Temp', 'Adjusted Temp'}, 'Location', 'best');
grid on;
saveas(gcf, 'C:/Users/HP/OneDrive/Desktop/AC_Simulator/results/temp_optimization_fig1.png', 'png');
disp('Figure 1 created');

% Figure 2: Energy Usage Trend
figure('Position', [700, 100, 600, 400]);
h3 = plot(time, energy, 'm-', 'LineWidth', 2, 'DisplayName', 'Energy Usage');
title('Energy Consumption Over 24 Hours');
xlabel('Time (minutes)');
ylabel('Energy Units');
legend(h3, 'Energy Usage', 'Location', 'best');
grid on;
saveas(gcf, 'C:/Users/HP/OneDrive/Desktop/AC_Simulator/results/temp_optimization_fig3.png', 'png');
disp('Figure 3 created');

% Figure 2: AC Settings Over Time (Simplified)
figure('Position', [100, 500, 600, 400]);
unique_settings = unique(settings);
colors = lines(length(unique_settings));
hold off;
h = [];
for i = 1:length(unique_settings)
    idx = strcmp(settings, unique_settings{i});
    if any(idx)
        h(end+1) = plot(time(idx), i * ones(sum(idx), 1), '.', 'Color', colors(i,:), 'MarkerSize', 10);
    end
end
if ~isempty(h)
    title('AC Settings Over Time');
    xlabel('Time (minutes)');
    ylabel('Setting Level');
    legend(unique_settings, 'Location', 'best'); % Simplified legend
    set(gca, 'YTick', 1:length(unique_settings), 'YTickLabel', unique_settings);
    grid on;
end
saveas(gcf, 'C:/Users/HP/OneDrive/Desktop/AC_Simulator/results/temp_optimization_fig2.png', 'png');
disp('Figure 2 created');

% Figure 4: Comfort Zone Analysis
figure('Position', [700, 500, 600, 400]);
comfort_flag = (adj_temp >= 22 & adj_temp <= 24);
h4 = plot(time, comfort_flag, 'g.', 'MarkerSize', 10, 'DisplayName', 'Comfort Zone');
title('Comfort Zone Occupancy');
xlabel('Time (minutes)');
ylabel('In Comfort Zone (1=Yes, 0=No)');
legend('Comfort Zone', 'Location', 'best');
grid on;
saveas(gcf, 'C:/Users/HP/OneDrive/Desktop/AC_Simulator/results/temp_optimization_fig4.png', 'png');
disp('Figure 4 created');

% Figure 5: Temperature Deviation
figure('Position', [100, 900, 600, 400]);
h5 = plot(time, temp_deviation, 'c-', 'LineWidth', 2, 'DisplayName', 'Temperature Deviation');
title('Cooling Effectiveness');
xlabel('Time (minutes)');
ylabel('Deviation (°C)');
legend('Temperature Deviation', 'Location', 'best');
grid on;
saveas(gcf, 'C:/Users/HP/OneDrive/Desktop/AC_Simulator/results/temp_optimization_fig5.png', 'png');
disp('Figure 5 created');

% Display completion message
disp('Visualizations saved as temp_optimization_fig1.png to temp_optimization_fig5.png');