using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.IO;
using System.Windows;
using System.Windows.Controls;

namespace PuzzleSolverFrontend
{
    public class PuzzleCell
    {
        public string Value { get; set; }
    }

    public partial class MainWindow : Window
    {
        private List<List<PuzzleCell>> puzzleRows = new List<List<PuzzleCell>>();

        public MainWindow()
        {
            InitializeComponent();
            GenerateGrid(3); // Default 3x3 grid
        }

        private void GenerateGrid(int size)
        {
            puzzleRows.Clear();
            for (int i = 0; i < size; i++)
            {
                var row = new List<PuzzleCell>();
                for (int j = 0; j < size; j++)
                {
                    row.Add(new PuzzleCell { Value = (i * size + j).ToString() });
                }
                puzzleRows.Add(row);
            }
            PuzzleInputGrid.ItemsSource = puzzleRows;
            PuzzleInputGrid.Items.Refresh();
        }

        private void GenerateGrid_Click(object sender, RoutedEventArgs e)
        {
            if (int.TryParse(SizeTextBox.Text, out int size) && size >= 2 && size <= 10)
            {
                GenerateGrid(size);
                StatusBarText.Text = $"Generated {size}x{size} grid";
            }
            else
            {
                MessageBox.Show("Please enter a valid size between 2 and 10", "Error", MessageBoxButton.OK, MessageBoxImage.Error);
            }
        }

        private void SolvePuzzle_Click(object sender, RoutedEventArgs e)
        {
            try
            {
                if (!int.TryParse(SizeTextBox.Text, out int size) || size < 2 || size > 10)
                {
                    MessageBox.Show("Invalid puzzle size", "Error", MessageBoxButton.OK, MessageBoxImage.Error);
                    return;
                }

                // Collect puzzle data
                List<string> puzzleLines = new List<string>();
                foreach (var row in puzzleRows)
                {
                    List<string> values = new List<string>();
                    foreach (var cell in row)
                    {
                        values.Add(cell.Value);
                    }
                    puzzleLines.Add(string.Join(" ", values));
                }

                // Get the path to the Python script
                string pythonScriptPath = Path.Combine(AppDomain.CurrentDomain.BaseDirectory, "puzzle.py");
                if (!File.Exists(pythonScriptPath))
                {
                    MessageBox.Show("Python script not found!", "Error", MessageBoxButton.OK, MessageBoxImage.Error);
                    return;
                }

                string method = AStarRadio.IsChecked == true ? "--astar" : "--bfs";
                string input = $"{size}\n{string.Join("\n", puzzleLines)}";

                // Configure process start info
                ProcessStartInfo start = new ProcessStartInfo
                {
                    FileName = "python",
                    Arguments = $"\"{pythonScriptPath}\" {method}",
                    UseShellExecute = false,
                    RedirectStandardInput = true,
                    RedirectStandardOutput = true,
                    RedirectStandardError = true,
                    CreateNoWindow = true
                };

                StatusBarText.Text = "Solving puzzle...";
                SolutionText.Text = "";

                // Run Python process
                using (Process process = Process.Start(start))
                {
                    // Send input to Python
                    using (StreamWriter sw = process.StandardInput)
                    {
                        sw.WriteLine(input);
                    }

                    // Read output
                    string output = process.StandardOutput.ReadToEnd();
                    string errors = process.StandardError.ReadToEnd();

                    process.WaitForExit();

                    if (!string.IsNullOrEmpty(errors))
                    {
                        SolutionText.Text = errors;
                        StatusBarText.Text = "Solution Found";
                    }
                    else
                    {
                        SolutionText.Text = output;
                        StatusBarText.Text = process.ExitCode == 0 ? "Solution found" : "No solution found";
                    }
                }
            }
            catch (Exception ex)
            {
                SolutionText.Text = $"Error: {ex.Message}";
                StatusBarText.Text = "Error occurred";
            }
        }
    }
}
