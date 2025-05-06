using Dragablz;
using Microsoft.Web.WebView2.Core;
using Microsoft.Web.WebView2.Wpf;
using System;
using System.Windows;
using System.Windows.Controls;

namespace SoulianaBrowser
{
    public partial class MainWindow : MahApps.Metro.Controls.MetroWindow
    {
        public MainWindow()
        {
            InitializeComponent();
            InitializeDefaultTabs();
        }

        private void InitializeDefaultTabs()
        {
            AddWebViewTab("https://bing.com");
            
        }

        private void AddWebViewTab(string url)
        {
            // Declare the TabItem variable
            TabItem tabItem = null;

            // Create a new WebView2 instance
            var webView = CreateWebView(url);

            // Create a close button for the tab
            var closeButton = new Button
            {
                Content = "X",
                Width = 20,
                Height = 20,
                Margin = new Thickness(5, 0, 0, 0)
            };
            closeButton.Click += (s, e) =>
            {
                TabControl.Items.Remove(tabItem);
            };

            // Create a header with the URL and close button
            var header = new StackPanel { Orientation = Orientation.Horizontal };
            header.Children.Add(new TextBlock { Text = url, VerticalAlignment = VerticalAlignment.Center });
            header.Children.Add(closeButton);

            // Create a new TabItem
            tabItem = new TabItem
            {
                Header = header,
                Content = webView
            };

            // Add the TabItem to the TabablzControl
            TabControl.Items.Add(tabItem);

            // Select the newly added tab
            TabControl.SelectedItem = tabItem;
        }

        private WebView2 CreateWebView(string url)
        {
            var webView = new WebView2();

            webView.Loaded += async (s, e) =>
            {
                try
                {
                    await webView.EnsureCoreWebView2Async();
                    webView.CoreWebView2.Navigate(url);
                }
                catch (Exception ex)
                {
                    MessageBox.Show("WebView2 Error: " + ex.Message);
                }
            };

            webView.HorizontalAlignment = HorizontalAlignment.Stretch;
            webView.VerticalAlignment = VerticalAlignment.Stretch;

            return webView;
        }

        private void AddNewTab_Click(object sender, RoutedEventArgs e)
        {
            AddWebViewTab("https://bing.com");
        }

        private void CloseAllTabs_Click(object sender, RoutedEventArgs e)
        {
            TabControl.Items.Clear();
        }

        private void NavigateToUrl_Click(object sender, RoutedEventArgs e)
        {
            if (TabControl.SelectedItem is TabItem selectedTab && selectedTab.Content is WebView2 webView)
            {
                var url = UrlTextBox.Text;
                if (!string.IsNullOrWhiteSpace(url))
                {
                    try
                    {
                        webView.CoreWebView2.Navigate(url);
                    }
                    catch (Exception ex)
                    {
                        MessageBox.Show("Navigation Error: " + ex.Message);
                    }
                }
            }
        }
    }
}
