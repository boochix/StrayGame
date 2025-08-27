using System;
using System.IO.Ports;
using System.Threading;
using UnityEngine;
using TMPro;

public class ESP32Controller : MonoBehaviour
{
    public TMP_Dropdown portDropdown;
    public TMP_Text statusText;
    public TMP_Text connectButtonLabel;  // ← Assign TMP text from your button

    private SerialPort serialPort;
    private Thread readThread;
    private bool isRunning = false;
    private bool isConnected = false;

    private string[] lastPorts;
    private float refreshTimer = 0f;
    private const float refreshInterval = 2f;

    void Start()
    {
        RefreshPortDropdown();
        UpdateButtonLabel();
    }

    void Update()
    {
        refreshTimer += Time.deltaTime;
        if (refreshTimer >= refreshInterval)
        {
            refreshTimer = 0f;
            RefreshPortDropdown();
        }
    }

    void RefreshPortDropdown()
    {
        string[] currentPorts = SerialPort.GetPortNames();

        if (lastPorts == null || !AreArraysEqual(lastPorts, currentPorts))
        {
            lastPorts = currentPorts;
            portDropdown.ClearOptions();

            if (currentPorts.Length > 0)
            {
                portDropdown.AddOptions(new System.Collections.Generic.List<string>(currentPorts));
                portDropdown.value = 0;
            }
            else
            {
                portDropdown.options.Add(new TMP_Dropdown.OptionData("No Ports Found"));
            }
        }
    }

    bool AreArraysEqual(string[] a, string[] b)
    {
        if (a.Length != b.Length) return false;
        for (int i = 0; i < a.Length; i++)
            if (a[i] != b[i]) return false;
        return true;
    }

    public void ToggleConnection()
    {
        if (isConnected)
        {
            DisconnectPort();
        }
        else
        {
            ConnectToSelectedPort();
        }
        UpdateButtonLabel();
    }

    void ConnectToSelectedPort()
    {
        if (portDropdown.options.Count == 0 || portDropdown.options[0].text == "No Ports Found")
        {
            statusText.text = "No port selected.";
            return;
        }

        string selectedPort = portDropdown.options[portDropdown.value].text;

        try
        {
            serialPort = new SerialPort(selectedPort, 115200);
            serialPort.Open();
            isRunning = true;
            isConnected = true;

            readThread = new Thread(ReadSerial);
            readThread.Start();

            statusText.text = $"Connected to {selectedPort}";
        }
        catch (Exception e)
        {
            statusText.text = $"Failed: {e.Message}";
            isConnected = false;
        }
    }

    void DisconnectPort()
    {
        if (serialPort != null && serialPort.IsOpen)
        {
            isRunning = false;
            readThread?.Join();
            serialPort.Close();
        }

        isConnected = false;
        statusText.text = "Disconnected.";
    }

    void UpdateButtonLabel()
    {
        connectButtonLabel.text = isConnected ? "Disconnect" : "Connect";
    }

    void ReadSerial()
    {
        while (isRunning && serialPort != null && serialPort.IsOpen)
        {
            try
            {
                string line = serialPort.ReadLine();
                Debug.Log("ESP32 says: " + line);
            }
            catch (TimeoutException) { }
            catch (Exception e)
            {
                Debug.LogWarning("Serial error: " + e.Message);
                isRunning = false;
                isConnected = false;
            }
        }
    }

    void OnApplicationQuit()
    {
        DisconnectPort();
    }
}
