app.post('/admin/options', (req, res) => {
    const optionsHtml = `<h1>Admin Page Options</h1>
      <form action="/admin/options" method="post">
        <button type="submit" name="option" value="viewAll">View All Appointments</button>
        <button type="submit" name="option" value="viewByDate">View by Date</button>
      </form>`;
  
    // Since you're using POST, access the option value from req.body.option
    if (req.body.option === 'viewAll') {
      res.redirect('/admin/appointments/all');
    } else if (req.body.option === 'viewByDate') {
      res.redirect('/admin/appointments/by-date');
    } else {
      res.send(optionsHtml);
    }
  }); 